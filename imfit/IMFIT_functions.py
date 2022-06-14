import psycopg2
import json


global sysID
global codeID
global planID


def set_systemid(connection, systemname):
    global sysID
    sysID = get_systemid(connection, systemname)
    return sysID


def set_codeid(connection, codename):
    global codeID
    codeID = (get_sourcecodeid(connection, codename))
    return codeID


def set_planid(connection, planname):
    global planID
    planID = get_FIplanid(connection, planname)
    return planID


def add_time_to_system(connection, time):
    try:
        cursor = connection.cursor()

        cursor.execute("UPDATE tblsystem SET timedata = %s WHERE systemid = %s",
                       (time, sysID))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns system id
def get_systemid(connection, systemname):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT systemid FROM tblsystem WHERE name= %s", (systemname,))
        myidtuple = cursor.fetchone()
        myid = myidtuple[0]
        cursor.close()
        return myid
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns sourcecode id
def get_sourcecodeid(connection, code_name):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT codeid FROM tblsourcecode WHERE codename= %s AND systemid = %s", (code_name, sysID,))
        myidtuple = cursor.fetchone()
        myid = myidtuple[0]
        print(myid)
        cursor.close()
        return myid
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Insert user's source code into database. Gets systemname paramater to find the which user is using
def insert_sourcecode(connection, code_name):
    try:
        cursor = connection.cursor()
        with open(code_name) as f:
            source_code = f.readlines()
        str_source_code = ''.join(source_code)
        cursor.execute("INSERT INTO tblsourcecode( systemid, codename, sourcecode) VALUES( %s, %s, %s)",
                       (sysID, code_name, str_source_code))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


def insert_sourcecodeWithStr(connection, codename, codestr):
    try:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO tblsourcecode( systemid, codename, sourcecode)
                                  SELECT %s, %s, %s
                                  WHERE NOT EXISTS(SELECT 1 FROM tblsourcecode WHERE systemid = %s AND codename = %s)""", (sysID, codename, codestr, sysID, codename))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Lists codes' file names from database which user selected
def list_sourcecodes(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT codename FROM tblsourcecode WHERE systemid= %s", (sysID,))
        mycodetuple = cursor.fetchall()
        print(mycodetuple)
        cursor.close()
        return mycodetuple
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns source code from database
def get_sourcecode(connection, codename):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT sourcecode FROM tblsourcecode WHERE codename= %s AND systemid = %s", (codename, sysID,))
        mycodetuple = cursor.fetchone()
        mycode = mycodetuple[0]
        print(mycode)
        cursor.close()
        return mycode
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Updates source code in database
def update_sourcecode(connection, file_name):
    try:
        cursor = connection.cursor()
        with open(file_name) as f:
            source_code = f.readlines()
        str_source_code = ''.join(source_code)
        cursor.execute("UPDATE tblsourcecode SET sourcecode = %s WHERE codeid = %s AND systemid = %s",
                       (str_source_code, codeID, sysID))
        updated_rows = cursor.rowcount
        print(updated_rows)
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


def update_sourcecode_withstr(connection, source_code_string):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE tblsourcecode SET sourcecode = %s WHERE codeid = %s AND systemid = %s",
                       (source_code_string, codeID, sysID))
        updated_rows = cursor.rowcount
        print(updated_rows)
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []



# Lists workloads
def list_workloads(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT workloadname FROM tblworkload WHERE codeid= %s", (codeID,))
        myworkloadtuple = cursor.fetchall()
        print(myworkloadtuple)
        cursor.close()
        return myworkloadtuple
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns workload data from workloadname
def get_workloaddata(connection, workloadname):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT data FROM tblworkload WHERE codeid= %s AND workloadname = %s", (codeID, workloadname))
        myworkloadtuple = cursor.fetchone()
        workloaddata = myworkloadtuple[0]
        print(workloaddata)
        cursor.close()
        return workloaddata
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns workloadtitle and workloadprocess
def get_workload(connection, workloadname):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT workloadtitle, workloadprocess FROM tblworkload WHERE codeid= %s AND workloadname = %s", (codeID, workloadname))
        myworkloadtuple = cursor.fetchall()
        print(myworkloadtuple)
        cursor.close()
        return myworkloadtuple
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Updates workload data in database
def update_workloaddata(connection, workloadname, workloaddata):
    try:
        cursor = connection.cursor()
        datastore = json.loads(workloaddata)
        new_data = json.dumps(datastore)
        cursor.execute("UPDATE tblworkload SET data = %s WHERE codeid = %s AND workloadname = %s",
                       (new_data, codeID, workloadname))
        updated_rows = cursor.rowcount
        print(updated_rows)
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# If workloadname has not already exists, Insert workload into database
def insert_workload(connection, workloadname, data, workloadtitle, workloadprocess):
    try:
        cursor = connection.cursor()
        datastore = json.loads(data)
        new_data = json.dumps(datastore)
        cursor.execute("""INSERT INTO tblworkload( codeid, workloadname, data, workloadtitle, workloadprocess)
                          SELECT %s, %s, %s, %s, %s
                          WHERE NOT EXISTS(SELECT 1 FROM tblworkload WHERE codeid = %s AND workloadname = %s)""",  (codeID, workloadname, new_data, workloadtitle, workloadprocess, codeID, workloadname))
        cursor.close()
        connection.commit()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# List code sinppets
def list_snippets(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT snippetname FROM tblsnippet WHERE codeid= %s", (codeID,))
        mysnippettuple = cursor.fetchall()
        print(mysnippettuple)
        cursor.close()
        return mysnippettuple
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns snippetregex data according to snippet name and code id
def get_snippetregex(connection, snippetname):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT regexcode FROM tblsnippet WHERE codeid= %s AND snippetname = %s", (codeID, snippetname))
        mysnippettuple = cursor.fetchone()
        mysnippetregex = mysnippettuple[0]
        print(mysnippetregex)
        cursor.close()
        return mysnippetregex
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns snippettitle data according to snippet name and code id
def get_snippettitle(connection, snippetname):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT snippettitle FROM tblsnippet WHERE codeid= %s AND snippetname = %s", (codeID, snippetname))
        mysnippettuple = cursor.fetchone()
        mysnippettitle = mysnippettuple[0]
        print(mysnippettitle)
        cursor.close()
        return mysnippettitle
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns snippetprocess data according to snippet name and code id
def get_snippetprocess(connection, snippetname):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT snippetprocess FROM tblsnippet WHERE codeid= %s AND snippetname = %s", (codeID, snippetname, ))
        mysnippettuple = cursor.fetchone()
        mysnippetprocess = mysnippettuple[0]
        print(mysnippetprocess)
        cursor.close()
        return mysnippetprocess
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# If snippetname has not already exists, Insert snippet into database
def insert_snippet(connection, snippetname, regexcode, snippettitle, snippetprocess):
    try:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO tblsnippet( codeid, snippetname, regexcode, snippettitle, snippetprocess) 
                        SELECT %s, %s, %s, %s, %s 
                        WHERE NOT EXISTS (SELECT 1 FROM tblsnippet WHERE codeid = %s AND snippetname = %s)""",
                       (codeID, snippetname, regexcode, snippettitle, snippetprocess, codeID, snippetname, ))
        cursor.close()
        connection.commit()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns line id
def get_lineid(connection, linename):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT lineid FROM tblline WHERE codeid= %s AND linename = %s", (codeID, linename, ))
        myidtuple = cursor.fetchone()
        myid = myidtuple[0]
        print(myid)
        cursor.close()
        return myid
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Insert line into database
def insert_line(connection, linename):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tblline( codeid, linename) VALUES( %s, %s)",
                       (codeID, linename, ))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


#List source code's lines
def list_lines(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT linename FROM tblline WHERE codeid= %s", (codeID, ))
        mylinetuple = cursor.fetchall()
        print(mylinetuple)
        cursor.close()
        connection.commit()
        return mylinetuple
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# INSERT orginalline into database
def insert_originalline(connection, linename, faultname):
    try:
        cursor = connection.cursor()
        lineid = get_lineid(connection, linename)
        faultid = get_faultid(connection, faultname)
        cursor.execute("INSERT INTO tbloriginalline( lineid, planid, faultid) VALUES( %s, %s, %s)",
                       (lineid, planID, faultid, ))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Lists originalline according to code id
def list_originallines_withcode(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT linename FROM tbloriginalline INNER JOIN tblline ON tbloriginalline.lineid = tblline.lineid WHERE tblline.codeid= %s", (codeID,))
        myoriginalline = cursor.fetchall()
        print(myoriginalline)
        cursor.close()
        return myoriginalline
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns FIPlan id from database
def get_FIplanid(connection, planname):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT planid FROM tblfiplan WHERE codeid= %s AND planname = %s", (codeID, planname, ))
        myplan = cursor.fetchone()
        plan =myplan[0]
        print(plan)
        cursor.close()
        return plan
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# List originallines according to FI plan
def list_originallinesfromFIplan(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT linename FROM tbloriginalline INNER JOIN tblline ON tbloriginalline.lineid = tblline.lineid INNER JOIN tblfiplan ON tbloriginalline.planid = tblfiplan.planid WHERE tblfiplan.planid= %s AND tblline.codeid = %s", (planID, codeID, ))
        myline = cursor.fetchone()
        print(myline)
        cursor.close()
        return myline
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns FIPlan context from database
def get_FIplancontext(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT tblline.linename, tblmutant.mutantlinename FROM tbloriginalline INNER JOIN tblline ON tbloriginalline.lineid = tblline.lineid INNER JOIN tblfiplan ON tbloriginalline.planid = tblfiplan.planid INNER JOIN tblmutant ON tbloriginalline.originallineid = tblmutant.originallineid WHERE tblfiplan.planid= %s AND tblfiplan.codeid = %s", (planID, codeID, ))
        plantuple = cursor.fetchall()
        print(plantuple[0][0])
        print(plantuple[0][1])
        connection.commit()
        cursor.close()
        return plantuple
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns FIPlans
def list_FIplans(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT planname FROM tblfiplan WHERE codeid= %s", (codeID,))
        myplantuple = cursor.fetchall()
        print(myplantuple)
        cursor.close()
        return myplantuple
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Insert FIPlan into database if not exists
def insert_FIplan(connection, planname):
    try:
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO tblfiplan (planname, codeid) 
                        SELECT %s, %s
                        WHERE NOT EXISTS(SELECT 1 FROM tblfiplan
                        WHERE planname=%s AND codeid=%s)""", (planname, codeID, planname, codeID, ))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns originallineid
def get_originallineid(connection, linename):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT tbloriginalline.originallineid FROM tbloriginalline INNER JOIN tblline ON tbloriginalline.lineid = tblline.lineid WHERE tblline.codeid = %s AND tblline.linename = %s", (codeID, linename))
        myline = cursor.fetchone()
        print(myline[0])
        cursor.close()
        return myline[0]
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Insert mutant line into database
def insert_mutant(connection, linename, mutantline):
    try:
        originallineid = get_originallineid(connection, linename)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tblmutant(originallineid, planid, mutantlinename) VALUES( %s, %s, %s)",
                       (originallineid, planID, mutantline))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns mutant line from database
def get_mutantline(connection, linename):
    try:
        originallineid = get_originallineid(connection, linename)
        cursor = connection.cursor()
        cursor.execute("SELECT mutantlinename FROM tblmutant  WHERE originallineid = %s AND planid = %s", (originallineid, planID, ))
        mymutantlinetuple = cursor.fetchone()
        print(mymutantlinetuple[0])
        cursor.close()
        return mymutantlinetuple[0]
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns faultid
def get_faultid(connection, faultname):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT faultid FROM tblfault WHERE faultname= %s AND planid= %s", (faultname, planID, ))
        myidtuple = cursor.fetchone()
        myid = myidtuple[0]
        cursor.close()
        return myid
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# If faultname exists, increase fault value. Otherwise insert faultname into database
def insert_fault(connection, faultname):
    try:
        #planid = get_FIplanid(connection, planname)
        cursor = connection.cursor()
        cursor.execute("""UPDATE tblfault SET faultvalue = faultvalue +1 WHERE planid=%s AND faultname=%s AND EXISTS(SELECT 1 FROM tblfault WHERE planid=%s AND faultname=%s);
                          INSERT INTO tblfault(planid ,faultname) select  %s, %s WHERE NOT EXISTS(SELECT 1 FROM tblfault WHERE planid=%s AND faultname=%s)
                            """, ( planID, faultname, planID, faultname, planID, faultname, planID, faultname))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Lists faults
def list_faults(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT faultname, faultvalue FROM tblfault  WHERE planid = %s", (planID,))
        faultuple=cursor.fetchall()
        print(faultuple)
        connection.commit()
        cursor.close()
        return faultuple
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Insert execution into database
def insert_execution(connection,  name, ubuntu, ros, python, gazebo, memory, timelimit):
    try:
        cursor = connection.cursor()
        # cursor.execute("""INSERT INTO tblexecution(name, ubuntu, ros, python, gazebo, memory, timelimit, codeid)
        #                   VALUES( %s, %s, %s, %s, %s, %s, %s, %s)""", (name, ubuntu, ros, python, gazebo, memory, timelimit, codeID))
        cursor.execute("""INSERT INTO tblexecution(name, ubuntu, ros, python, gazebo, memory, timelimit, codeid) 
                                  SELECT %s, %s, %s, %s, %s, %s, %s, %s
                                  WHERE NOT EXISTS (SELECT 1 FROM tblexecution where name = %s)""",
                       (name, ubuntu, ros, python, gazebo, memory, timelimit, codeID, name))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns execution values from database
def get_execution(connection, executionname):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name, ubuntu, ros, python, gazebo, memory, timelimit FROM tblexecution WHERE name = %s AND codeid = %s", (executionname, codeID))
        execution_values = cursor.fetchall()
        print(execution_values)
        connection.commit()
        cursor.close()
        return execution_values
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Lists execution names
def list_executions(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM tblexecution WHERE codeid=%s", (codeID,))
        myexecution = cursor.fetchall()
        print(myexecution)
        connection.commit()
        cursor.close()
        return myexecution
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Return execution id according to code id and execution name
def get_executionid(connection, name):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT executionid FROM tblexecution WHERE name = %s AND codeid = %s", (name, codeID, ))
        myline = cursor.fetchone()
        print(myline[0])
        cursor.close()
        return myline[0]
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Updates execution name
def update_executionname(connection, name):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE tblexecution SET name = %s WHERE name = %s AND codeid = %s",
                       (name, name, codeID))
        updated_rows = cursor.rowcount
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Updates execution ubuntu
def update_executionubuntu(connection, name, ubuntu):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE tblexecution SET ubuntu = %s WHERE name = %s AND codeid = %s",
                       (ubuntu, name, codeID))
        updated_rows = cursor.rowcount
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Updates execution ros
def update_executionros(connection, name, ros):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE tblexecution SET ros = %s WHERE name = %s AND codeid = %s",
                       (ros, name, codeID))
        updated_rows = cursor.rowcount
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Updates execution python
def update_executionpython(connection, name, python):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE tblexecution SET python = %s WHERE name = %s AND codeid = %s",
                       (python, name, codeID))
        updated_rows = cursor.rowcount
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Updates execution gazebo
def update_executiongazebo(connection, name, gazebo):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE tblexecution SET gazebo = %s WHERE name = %s AND codeid = %s",
                       (gazebo, name, codeID))
        updated_rows = cursor.rowcount
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Updates execution memory
def update_executionmemory(connection, name, memory):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE tblexecution SET memory = %s WHERE name = %s AND codeid = %s",
                       (memory, name, codeID))
        updated_rows = cursor.rowcount
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Updates execution timelimit
def update_executiontimelimit(connection, name, timelimit):
    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE tblexecution SET timelimit = %s WHERE name = %s AND codeid = %s",
                       (timelimit, name, codeID))
        updated_rows = cursor.rowcount
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Insert metric into database
def insert_metric(connection, executionname, metricname, metricvalue):
    try:
        cursor = connection.cursor()
        executionid = get_executionid(connection, executionname)
        cursor.execute("INSERT INTO tblmetric(planid, executionid, metricname, metricvalue) VALUES( %s, %s, %s, %s)",
                       (planID, executionid, metricname, metricvalue))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Lists metrics' names and values
def list_metrics(connection, executionname):
    try:
        cursor = connection.cursor()
        executionid = get_executionid(connection, executionname)
        cursor.execute("SELECT metricname, metricvalue FROM tblmetric WHERE executionid = %s AND planid = %s",
                       (executionid, planID))
        metrics = cursor.fetchall()
        print(metrics[0])
        cursor.close()
        return metrics
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Insert states' name and value into database
def insert_state(connection, executionname, statename, statevalue):
    try:
        cursor = connection.cursor()
        executionid = get_executionid(connection, executionname)
        cursor.execute("INSERT INTO tblstate(planid, executionid, statename, statevalue) VALUES( %s, %s, %s, %s)",
                       (planID, executionid, statename, statevalue))
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Lists states
def list_states(connection, executionname):
    try:
        cursor = connection.cursor()
        executionid = get_executionid(connection, executionname)
        cursor.execute("SELECT statename, statevalue FROM tblstate WHERE executionid = %s AND planid = %s",
                       (executionid, planID))
        statetuple = cursor.fetchall()
        print(statetuple)
        connection.commit()
        cursor.close()
        return statetuple
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Insert rosbag into database
def insert_rosbag(connection, executionname, rosbagname, rosbagdata):
    try:
        cursor = connection.cursor()
        executionid = get_executionid(connection, executionname)
        cursor.execute("INSERT INTO tblrosbag(planid, executionid, rosbagname, rosbagdata) VALUES( %s, %s, %s, %s)",
                       (planID, executionid, rosbagname, rosbagdata))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns rosbagdata
def get_rosbagdata(connection, executionname):
    try:
        cursor = connection.cursor()
        executionid = get_executionid(connection, executionname)
        cursor.execute("SELECT rosbagdata FROM tblrosbag WHERE executionid = %s AND planid = %s",
                       (executionid, planID))
        rosbagdata = cursor.fetchone()
        print(rosbagdata)
        connection.commit()
        cursor.close()
        return rosbagdata
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Lists rosbag files from database
def list_rosbags(connection, executionname):
    try:
        cursor = connection.cursor()
        executionid = get_executionid(connection, executionname)
        cursor.execute("SELECT rosbagname FROM tblrosbag WHERE executionid = %s AND planid = %s",
                       (executionid, planID))
        rosbagtuple = cursor.fetchall()
        print(rosbagtuple)
        connection.commit()
        cursor.close()
        return rosbagtuple
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Insert reports into database
def insert_report(connection, executionname, ast, pdfname, mutationscore):
    try:
        cursor = connection.cursor()
        executionid = get_executionid(connection, executionname)
        doc = open(pdfname+'.pdf', 'rb').read()
        cursor.execute("INSERT INTO tblreport(planid, executionid, astdiagram, pdfname, mutationscore, pdfdata) VALUES( %s, %s, %s, %s, %s, %s)",
                       (planID, executionid, ast, pdfname, mutationscore, doc))
        connection.commit()
        cursor.close()
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns mutation score from table report
def get_mutation_score(connection, planname, executionname):
    try:
        cursor = connection.cursor()
        executionid = get_executionid(connection, executionname)
        planid = get_FIplanid(connection, planname)
        cursor.execute("SELECT mutationscore FROM tblreport WHERE executionid = %s AND planid = %s", (executionid, planid, ))
        mutationscoretuple = cursor.fetchone()
        print(mutationscoretuple)
        connection.commit()
        cursor.close()
        return mutationscoretuple
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns pdf from table report
def get_pdf(connection, executionname):
    try:
        cursor = connection.cursor()
        executionid = get_executionid(connection, executionname)
        cursor.execute("SELECT pdfname, pdfdata FROM tblreport WHERE executionid = %s AND planid = %s", (executionid, planID, ))
        pdf = cursor.fetchone()
        print(pdf)
        connection.commit()
        cursor.close()
        return pdf
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


# Returns ast diagram from table report
def get_astdiagram(connection, planname, executionname):
    try:
        cursor = connection.cursor()
        executionid = get_executionid(connection, executionname)
        planid = get_FIplanid(connection, planname)
        cursor.execute("SELECT astdiagram FROM tblreport WHERE executionid = %s AND planid = %s", (executionid, planid, ))
        ast = cursor.fetchone()
        print(ast)
        connection.commit()
        cursor.close()
        return ast
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


