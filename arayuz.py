
import os.path
from PyQt5.QtWidgets import QFileDialog
import rosmonitoring.configSelect as configSelect
import rosmonitoring.configInsert as configInsert
import rosmonitoring.propertySelectInsert
import rosmonitoring.propertySelectInsert as propertySelectInsert
import rosmonitoring.configSelectOffline as configSelectOffline
import rosmonitoring.configInsertOffline as configInsertOffline
import uppaal.uppaalInsert as uppaalInsert
import uppaal.uppaalSelect as uppaalSelect

import json
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QMainWindow
from IMFITnUPPAAL import Ui_IMFIT
import imfit.IMFIT_functions as IMFITDB
import webbrowser
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Arayuz(QMainWindow):

    def __init__(self, connection):
        super().__init__()
        self.ui = Ui_IMFIT()
        self.ui.setupUi(self)
        self.UiComponents()
        self.connection = connection
        self.systemid = None
        self.codeid = None
        self.fiplanid = None
        #self.initUppaalROSMSettings()
        self.resizeWindow()


    def UiComponents(self):
        self.ui.tabWidgetDB.currentChanged.connect(self.resizeWindow)
        #imfit
        self.ui.btn_EnterSystemname.clicked.connect(self.btnEnterSystemname)
        self.ui.btn_ListCodes.clicked.connect(self.list_SourceCodes)
        self.ui.btn_CreateLines.clicked.connect(self.list_lines)
        self.ui.btn_ListExecutions.clicked.connect(self.list_executions)
        self.ui.btn_ListData.clicked.connect(self.show_metrics_states)
        self.ui.btn_ShowResults.clicked.connect(self.show_results)
        self.ui.btn_ShowPDF.clicked.connect(self.show_pdf)
        self.ui.btn_SendMailPDF.clicked.connect(self.send_email)
        self.ui.comboBoxSourceCodes.activated.connect(self.getCodeID)
        self.ui.comboBoxWorkloads.activated.connect(self.get_workloadcontext)
        self.ui.comboBoxFIPlans.activated.connect(self.getPlanID)
        self.ui.comboBoxExecutions.activated.connect(self.get_execution)
        self.ui.comboBoxRosbag.activated.connect(self.show_rosbagdata)
        self.ui.btn_InsertSourceCode.clicked.connect(self.insertSourceCode)
        #uppaal
        self.ui.comboBoxModelConfigFileList.activated.connect(self.cBox_selectConfig)
        self.ui.btn_ExportFile.clicked.connect(self.btn_exportConfigSet)
        self.ui.btn_InsertFile.clicked.connect(self.btn_importConfig)
        self.ui.btn_ROSSet.clicked.connect(self.btn_importConfigSet)
        self.ui.btn_AddProperty.clicked.connect(self.btn_addProperty)
        self.ui.btn_QIROSSet.clicked.connect(self.btn_saveProperty)
        #rosmonitoring
        self.ui.comboBoxModelList.activated.connect(self.cBox_selectXml)
        self.ui.btn_ImportUPPAALModel.clicked.connect(self.btn_importXml)
        self.ui.btn_ExportModel.clicked.connect(self.btn_exportXmlSet)
        self.ui.btn_UPPAALSet.clicked.connect(self.btn_importXmlSet)


    def resizeWindow(self):
        if self.ui.tabWidgetDB.currentIndex() == 0:
            self.resize(1270, 1018)
        else:
            self.resize(890, 550)


    def initUppaalROSMSettings(self):
        self.fillUppaalModels()
        self.fillConfigFiles()
        self.ui.textSelectedModelInfo.setFontPointSize(10)
        self.ui.textSelectedConfigFileInfo.setFontPointSize(10)

    # ROSMonitoring Functions


    def fillConfigFiles(self):
        self.ui.comboBoxModelConfigFileList.clear()
        configList = configSelect.selectAllOnlineConfigs(self.connection)
        configList += configSelectOffline.selectAllOfflineConfigs(self.connection)
        for i in configList:
            self.ui.comboBoxModelConfigFileList.addItem(str(i[0]) + '-' + str(i[1]) + '-' + str(i[2]) + '-' + str(i[3]))
        self.ui.comboBoxModelConfigFileList.setCurrentIndex(-1)

    def btn_saveProperty(self):
        rosmonitoring.propertySelectInsert.insertProperty(self.connection, self.ui.textQIROSVisible2.toPlainText(),
            self.ui.textQIROSVisible3.toPlainText(), self.ui.textQIROSVisible1.toPlainText(),
            self.ui.textQIROSVisible4.toPlainText(), self.ui.comboBoxModelConfigFileList.currentText().split('-')[1])
        self.ui.textQIROSVisible1.clear()
        self.ui.textQIROSVisible2.clear()
        self.ui.textQIROSVisible3.clear()
        self.ui.textQIROSVisible4.clear()
        self.ui.groupBoxQIROSGetInformation.setVisible(False)
        self.cBox_selectConfig()

    def btn_addProperty(self):
        if self.ui.comboBoxModelConfigFileList.currentText() != "":
            self.ui.groupBoxQIROSGetInformation.setVisible(True)

    def btn_importConfigSet(self):
        fname, filter = QFileDialog.getOpenFileName(self, 'Select config file', '', 'Graph (*.yaml);;All files (*)')
        if fname and self.ui.textROSVisible1.toPlainText().isdigit():
            if self.ui.radioButtonOnline.isChecked():
                configInsert.insertConfigFile(self.connection, fname, int(self.ui.textROSVisible1.toPlainText()))
            elif self.ui.radioButtonOffline.isChecked():
                configInsertOffline.insertConfigFile(self.connection, fname, int(self.ui.textROSVisible1.toPlainText()))
            self.fillConfigFiles()
        self.ui.textROSVisible1.clear()
        self.ui.groupBoxROSGetInformation_2.setVisible(False)

    def btn_exportConfigSet(self):
        if self.ui.comboBoxModelConfigFileList.currentText() == "":
            return
        directory = QFileDialog.getExistingDirectory(self, 'Select directory to save config file', '')
        if directory:
            directory = directory.replace('/', '\\')
            selectedText = self.ui.comboBoxModelConfigFileList.currentText()
            fileFullName = os.path.join(directory, selectedText.replace(" ", "").replace(':', '') + ".txt")
            f = open(fileFullName, "w+")
            if selectedText.split('-')[3] == 'online':
                f.write(configSelect.selectConfigFile(self.connection, int(selectedText.split('-')[2])))
            elif selectedText.split('-')[3] == 'offline':
                f.write(configSelectOffline.selectConfigFile(self.connection, int(selectedText.split('-')[2])))

    def btn_importConfig(self):
        self.ui.groupBoxROSGetInformation_2.setVisible(True)

    def cBox_selectConfig(self):
        selectedText = self.ui.comboBoxModelConfigFileList.currentText()
        selectedInfo = configSelect.selectConfigSystemInfo(self.connection, selectedText.split('-')[0])
        infoStr = "SystemID: " + selectedText.split('-')[0]
        infoStr += "\nSystem Name: " + selectedInfo[0]
        infoStr += "\nSystem Description: " + selectedInfo[1]
        infoStr += "\nMonitorID: " + selectedText.split('-')[1]
        infoStr += "\nOnlineID: " + selectedText.split('-')[2]

        self.ui.textSelectedConfigFileInfo.setText(infoStr)

        prpInfo = ""
        selectedPrpInfo = propertySelectInsert.selectProperties(self.connection, selectedText.split('-')[1])
        if selectedPrpInfo.__len__() > 0:
            for prp in selectedPrpInfo:
                prpInfo += "Dsc: " + prp[0]
                prpInfo += "\nLanguage: " + prp[1]
                prpInfo += "\nResult: " + str(prp[3])
                prpInfo += "\nCode: " + prp[2] + "\n---\n"
        else:
            prpInfo = "No properties found!"

        self.ui.textQueries.setText(prpInfo)

    # end ROSMonitoring Functions

    # uppaal functions

    def fillUppaalModels(self):
        self.ui.comboBoxModelList.clear()
        modelList = uppaalSelect.getAllUppaalRecords(self.connection)
        for i in modelList:
            self.ui.comboBoxModelList.addItem(i[1] + ' sysID:' + str(i[0]))
        self.ui.comboBoxModelList.setCurrentIndex(-1)

    def btn_importXmlSet(self):
        fname, filter = QFileDialog.getOpenFileName(self, 'Select xml file', '', 'Graph (*.xml);;All files (*)')
        if fname and self.ui.textUPPAALVisible1.toPlainText().isdigit():
            uppaalInsert.insertXmlFile(self.connection, fname, int(self.ui.textUPPAALVisible1.toPlainText()),
                                       self.ui.textUPPAALVisible2.toPlainText())
            self.fillUppaalModels()
        self.ui.textUPPAALVisible1.clear()
        self.ui.textUPPAALVisible2.clear()
        self.ui.groupBoxGetInformation.setVisible(False)

    def btn_exportXmlSet(self):
        if self.ui.comboBoxModelList.currentText() == "":
            return
        directory = QFileDialog.getExistingDirectory(self, 'Select directory to save xml file', '')
        if directory:
            directory = directory.replace('/', '\\')
            fileFullName = os.path.join(directory, self.ui.comboBoxModelList.currentText().replace(" ", "").replace(':', '') + ".txt")
            f = open(fileFullName, "w+")
            selectedText = self.ui.comboBoxModelList.currentText()
            f.write(uppaalSelect.selectUppaalModelXml(self.connection, int(selectedText.split(':')[1])))

    def btn_importXml(self):
        self.ui.groupBoxGetInformation.setVisible(True)

    def cBox_selectXml(self):
        selectedText = self.ui.comboBoxModelList.currentText()
        info = uppaalSelect.selectUppaalModelInfo(self.connection, int(selectedText.split(':')[1]))
        self.ui.textSelectedModelInfo.setText("SystemID: " + str(info[0]) + "\nModelID: " + str(info[1]) + "\nDesciption: " + str(info[3]) + "\nCreate Date: " + str(info[2]))
        #queries
        queryInfo = uppaalSelect.selectUppaalQueries(self.connection, info[1])
        self.ui.textSelectedModelQuery.clear()
        if queryInfo.__len__() > 0:
            for query in queryInfo:
                infoStr = query[0]
                infoStr += "\nDesc: " + query[1]
                infoStr += "\nResult Bit: " + str(query[2]) + "\n\n"
                self.ui.textSelectedModelQuery.append(infoStr)
        else:
            self.ui.textSelectedModelQuery.setText("No Queries Found!")

    # end uppaal functions

    # imfit functions

    def insertSourceCode(self):
        IMFITDB.insert_sourcecodeWithStr(self.connection, 'abs.py', 'python içerik')

    def btnEnterSystemname(self):
        self.connection.rollback()
        self.connection.autocommit = True
        systemname = self.ui.lineEditSystemname.text()
        self.systemid = IMFITDB.get_systemid(self.connection, systemname)
        self.systemid = IMFITDB.set_systemid(self.connection, systemname)
        if self.systemid:
            msgBox = QMessageBox()
            msgBox.setStyleSheet("background-color: rgb(211, 211, 211);\n""color: rgb(0, 0, 0);")
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText('Entered ' + systemname + ' Successfully')
            msgBox.setWindowTitle('INFO')
            msgBox.exec()
        else:
            msgBox = QMessageBox()
            msgBox.setStyleSheet("background-color: rgb(211, 211, 211);\n""color: rgb(0, 0, 0);")
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText('Invalid System name \nPlease Enter Valid System Name')
            msgBox.setWindowTitle('ERROR')
            msgBox.exec()

    def getCodeID(self):
        codename = self.ui.comboBoxSourceCodes.currentText()
        self.codeid = IMFITDB.get_sourcecodeid(self.connection, codename)
        self.codeid = IMFITDB.set_codeid(self.connection, codename)
        self.clearui()
        self.list_workloads()
        self.list_FIPlans()
        code_context = IMFITDB.get_sourcecode(self.connection, codename)
        self.ui.textSourceCode.setText(code_context)
        self.list_snippets()

    def get_workloadcontext(self):
        try:
            workloadname = self.ui.comboBoxWorkloads.currentText()
            workload_data = IMFITDB.get_workloaddata(self.connection, workloadname)
            str_workload = json.dumps(workload_data, indent=2, separators=(',', ': '))
            print(str_workload)
            self.ui.textWorkload.setText(str_workload)
        except Exception as err:
            print(str(err))

    def getPlanID(self):
        planname = self.ui.comboBoxFIPlans.currentText()
        self.fiplanid = IMFITDB.set_planid(self.connection, planname)
        self.ui.textOriginalLine.clear()
        self.ui.textMutated.clear()
        fiplan = IMFITDB.get_FIplancontext(self.connection)
        self.ui.textOriginalLine.append(fiplan[0][0])
        self.ui.textMutated.append(fiplan[0][1])

    def get_execution(self):
        executionname = self.ui.comboBoxExecutions.currentText()
        planname = self.ui.comboBoxFIPlans.currentText()
        execution_values = IMFITDB.get_execution(self.connection, executionname)
        self.ui.textName.setText(execution_values[0][0])
        self.ui.textOS.setText(execution_values[0][1])
        self.ui.textROS.setText(execution_values[0][2])
        self.ui.textPython.setText(execution_values[0][3])
        self.ui.textGazebo.setText(execution_values[0][4])
        self.ui.textMemorySize.setText(str(execution_values[0][5]))
        self.ui.textTimeLimit.setText(str(execution_values[0][6]))
        self.ui.textSelectedFIPlan.setText(planname)

    def list_SourceCodes(self):
        sourcecodelist = IMFITDB.list_sourcecodes(self.connection)
        for name in sourcecodelist:
            self.ui.comboBoxSourceCodes.addItem(name[0])

    def list_workloads(self):
        workloadlist = IMFITDB.list_workloads(self.connection)
        for name in workloadlist:
            self.ui.comboBoxWorkloads.addItem(name[0])

    def list_FIPlans(self):
        fiplanlist = IMFITDB.list_FIplans(self.connection)
        for name in fiplanlist:
            self.ui.comboBoxFIPlans.addItem(name[0])

    def list_lines(self):
        if self.codeid:
            lines = IMFITDB.list_lines(self.connection)
            self.ui.textLines.clear()
            for line in lines:
                self.ui.textLines.append(line[0])
            self.getPlanID()
        else:
            msgBox = QMessageBox()
            msgBox.setStyleSheet("background-color: rgb(211, 211, 211);\n""color: rgb(0, 0, 0);")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Please Select Source Code')
            msgBox.setWindowTitle('Warning')
            msgBox.exec()

    def list_snippets(self):
        snippets = IMFITDB.list_snippets(self.connection)
        for snippet in snippets:
            self.ui.textSnippets.append(snippet[0])

    def list_executions(self):
        executionlist = IMFITDB.list_executions(self.connection)
        self.ui.comboBoxExecutions.clear()
        for name in executionlist:
            self.ui.comboBoxExecutions.addItem(name[0])

    def show_pdf(self):
        executionname = self.ui.comboBoxExecutions.currentText()
        planname = self.ui.comboBoxFIPlans.currentText()
        pdf = IMFITDB.get_pdf(self.connection, planname, executionname)
        pdfname = pdf[0]
        pdfdata = pdf[1]
        self.ui.labelPDFname.setText(pdfname)
        with open(pdfname + '.pdf', 'wb') as file:
            file.write(pdfdata)
        dir = os.getcwd()
        print(dir)
        webbrowser.open_new(dir + '\\' + pdfname + '.pdf')

    def show_results(self):
        executionname = self.ui.comboBoxExecutions.currentText()
        planname = self.ui.comboBoxFIPlans.currentText()
        if executionname != '' and planname != '':
            self.ui.textReport.clear()
            self.ui.comboBoxRosbag.clear()
            try:
                ast_data = IMFITDB.get_astdiagram(self.connection, planname, executionname)

                rosbags = IMFITDB.list_rosbags(self.connection, planname, executionname)
                for rosbag in rosbags:
                    self.ui.comboBoxRosbag.addItem(str(rosbag[0]))

                metrics = IMFITDB.list_metrics(self.connection, planname, executionname)
                for metric in metrics:
                    self.ui.textReport.append(metric[0] + '\t\t    ' + str(metric[1]))

                states = IMFITDB.list_states(self.connection, planname, executionname)
                for state in states:
                    self.ui.textReport.append(state[0] + '\t\t    ' + str(state[1]))

                faults = IMFITDB.list_faults(self.connection, planname)
                for fault in faults:
                    self.ui.textReport.append(fault[0] + '\t\t    ' + str(fault[1]))

                self.ui.textAST.setText(ast_data[0])

                mutationscore = IMFITDB.get_mutation_score(self.connection, planname, executionname)
                self.ui.textReport.append('Mutation Score' + '\t\t    ' + str(mutationscore[0]))
            except:
                print("ERROROR")

        else:
            msgBox = QMessageBox()
            msgBox.setStyleSheet("background-color: rgb(211, 211, 211);\n""color: rgb(0, 0, 0);")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Select Execution and FI Plan')
            msgBox.setWindowTitle('Warning')
            msgBox.exec()

    def show_rosbagdata(self):
        executionname = self.ui.comboBoxExecutions.currentText()
        planname = self.ui.comboBoxFIPlans.currentText()
        rosbag = IMFITDB.get_rosbagdata(self.connection, planname, executionname)
        self.ui.textRosbagScenario.setText(rosbag[0])

    def show_metrics_states(self):
        executionname = self.ui.comboBoxExecutions.currentText()
        planname = self.ui.comboBoxFIPlans.currentText()
        self.ui.textStates.clear()
        self.ui.textMetrics.clear()
        metrics = IMFITDB.list_metrics(self.connection, planname, executionname)
        states = IMFITDB.list_states(self.connection, planname, executionname)
        if planname != '' and executionname != '':
            if metrics:
                for metric in metrics:
                    self.ui.textMetrics.append(str(metric[0]))
            else:
                msgBox = QMessageBox()
                msgBox.setStyleSheet("background-color: rgb(211, 211, 211);\n""color: rgb(0, 0, 0);")
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('There is no metrics')
                msgBox.setWindowTitle('Warning')
                msgBox.exec()

            if states:
                for state in states:
                    self.ui.textStates.append(str(state[0]))
            else:
                msgBox = QMessageBox()
                msgBox.setStyleSheet("background-color: rgb(211, 211, 211);\n""color: rgb(0, 0, 0);")
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.setText('There is no states')
                msgBox.setWindowTitle('Warning')
                msgBox.exec()
        else:
            msgBox = QMessageBox()
            msgBox.setStyleSheet("background-color: rgb(211, 211, 211);\n""color: rgb(0, 0, 0);")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText('Please Select FIPlan and Execution')
            msgBox.setWindowTitle('Warning')
            msgBox.exec()

    def send_email(self):
        executionname = self.ui.comboBoxExecutions.currentText()
        planname = self.ui.comboBoxFIPlans.currentText()
        pdf = IMFITDB.get_pdf(self.connection, planname, executionname)
        pdfnamee = pdf[0]
        pdfdata = pdf[1]
        self.ui.labelPDFname.setText(pdfnamee)
        body = ''' IM-FIT Report is attached. '''
        sender = 'vvdbtool@gmail.com'
        password = 'vvdb5159'
        receiver = self.ui.lineEditSendMailPDF.text()
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = 'VV Database Tool Report'
        message.attach(MIMEText(body, 'plain'))
        pdfname = pdfnamee
        bytea = pdfdata
        file = open(pdfname + '.pdf', 'wb')
        file.write(bytea)
        file.close()
        pdfname2 = pdfname + '.pdf'
        binary_pdf = open(pdfname2, 'rb')
        payload = MIMEBase('application', 'octate-stream', Name=pdfname2)
        payload.set_payload((binary_pdf).read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Decomposition', 'attachment', filename=pdfname2)
        message.attach(payload)
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender, password)
        text = message.as_string()
        session.sendmail(sender, receiver, text)
        session.quit()
        print('Mail Sent')

    def btnClearInfos(self):
        self.ui.textSourceCode.clear()
        self.ui.textWorkload.clear()
        self.ui.textReport.clear()
        self.ui.textAST.clear()
        self.ui.textRosbagScenario.clear()
        self.ui.textMutated.clear()
        self.ui.textOriginalLine.clear()

    def clearui(self):
        self.ui.textSourceCode.clear()
        self.ui.textWorkload.clear()
        self.ui.textSnippets.clear()
        self.ui.textLines.clear()
        self.ui.comboBoxWorkloads.clear()
        self.ui.comboBoxFIPlans.clear()

    def btnClickClearComboBoxExec(self):
        self.ui.comboBoxFIPlans.clear()
        self.ui.comboBoxExecutions.clear()

    # end imfit functions