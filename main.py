import dbConnection
from PyQt5.QtWidgets import *
import sys
from arayuz import Arayuz
import imfit.IMFIT_functions as IMFITDB


def start():
    qApp = QApplication(sys.argv)
    win = Arayuz(connection)
    win.show()
    sys.exit(qApp.exec())


connection = dbConnection.connect("postgres", "postgres", "2415")

# functions comes here
# connection.commit()
IMFITDB.set_systemid(connection, 'system1')
# IMFITDB.insert_sourcecodeWithStr(connection, 'SOURCE CODE', 'CONTENT\\n xd')
#IMFITDB.update_sourcecode_withstr(connection, 'updated source code data')
IMFITDB.set_codeid(connection, 'SOURCE CODE')
#IMFITDB.insert_workload(connection, 'WORKLOAD TEST', '{"name": "Bob", "languages": "English"}', 'workload title', 'workload process')
# workloads= IMFITDB.list_workloads(connection)
#print(workloads)
#IMFITDB.update_workloaddata(connection, 'WORKLOAD TEST', '{"name": "Bab", "languages": "English"}')
#IMFITDB.insert_snippet(connection, 'testsnipttet', 'regex', 'sniptitle', 'snipproces')
#IMFITDB.list_snippets(connection)
#IMFITDB.insert_line(connection, 'testsatiri')
#IMFITDB.list_lines(connection)
#IMFITDB.insert_FIplan(connection, 'testfiplan2')
IMFITDB.set_planid(connection, 'testfiplan2')
#IMFITDB.list_FIplans(connection)

#IMFITDB.insert_fault(connection, 'testfault')
#IMFITDB.insert_fault(connection, 'testfault2')
#IMFITDB.list_faults(connection)

#IMFITDB.insert_originalline(connection, 'testsatiri', 'testfault2')
#IMFITDB.list_originallinesfromFIplan(connection)
#IMFITDB.get_originallineid(connection, 'testsatiri')

#IMFITDB.insert_mutant(connection, 'testsatiri', 'mutanttestsatiri')
#IMFITDB.get_mutantline(connection, 'testsatiri')

#IMFITDB.get_FIplancontext(connection)

#IMFITDB.insert_execution(connection, 'testexec3', 't_ubuntu', 't_ros', 't_python', 't_gazebo', 65, 45)
#IMFITDB.get_execution(connection, 'testexec')
#IMFITDB.get_executionid(connection, 'testexec')
#IMFITDB.list_executions(connection)
#IMFITDB.update_executiongazebo(connection, 'testexec3', 'updatedgazebo')

#IMFITDB.insert_metric(connection, 'testexec3', 'testmetric', 521)
#IMFITDB.list_metrics(connection, 'testexec3')

#IMFITDB.insert_state(connection, 'testexec3', 'teststatae' , 214321)
#IMFITDB.list_states(connection, 'testexec3')

# IMFITDB.insert_rosbag(connection, 'testexec3', 'testrosbagnname', 'testrosbagdata')
# IMFITDB.get_rosbagdata(connection, 'testexec3')
# IMFITDB.insert_rosbag(connection, 'testexec3', 'testrosbagnname2', 'testrosbagdata2')
# IMFITDB.list_rosbags(connection, 'testexec3')

#IMFITDB.insert_report(connection, 'testexec3')
#start()
connection.close()



''' TEST main
test.sourcecode_insert('system1', 'abstraction.py') 
test.get_sourcecode('abstraction.py')
test.list_sourcecodes(3)
test.sourcecode_update('abstraction.py', 3)
test.get_sourcecode('abstraction.py')
'''
'''Testing for try catch
test.sourcecode_insert('xd', 'abstraction.py')
'''

''' jsonb insert
with open('ornek_json.json', 'r') as f:
    datastore = json.load(f)
n_data = json.dumps(datastore)
print(datastore)
print(n_data)
print(datastore["gorevler"][0]["Task"]["Task_ID"])
query = "INSERT INTO tblworkload( codeid, workloadname, data, workloadtitle, workloadprocess) VALUES( 1, 'workload1',%s,'title1','process1')"
cursor.execute(query, (n_data, ))
'''

'''pdf insert
cursor = connection.cursor()
doc = open('testpdf.pdf', 'rb').read()
cursor.execute("INSERT INTO tblreport(planid, executionid, astdiagram, pdfname, mutationscore, pdfdata) VALUES(2, 1,'asttest2', 'testpdf', 105, %s)",(doc, ))
'''

'''
cursor = connection.cursor()
cursor.execute("SELECT pdfname, pdfdata FROM tblreport WHERE pdfname='testpdf'")
mypdfdata = cursor.fetchone()
with open(mypdfdata[0]+'.pdf', 'wb') as file:
    file.write(mypdfdata[1])

connection.commit()
connection.close()
cursor.close()
'''

'''
query = "SELECT sourcecode FROM tblsourcecode WHERE codeid=1"

resList = dbFuncs.runQuery(connection, query)
dbFuncs.printTable(resList)
'''



