import dbConnection
from PyQt5.QtWidgets import *
import sys
from arayuz import Arayuz


def start():
    qApp = QApplication(sys.argv)
    win = Arayuz(connection)
    win.show()
    sys.exit(qApp.exec())


connection = dbConnection.connect("VVToolDataBase", "postgres", "241559")

# functions comes here
connection.commit()
start()
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



