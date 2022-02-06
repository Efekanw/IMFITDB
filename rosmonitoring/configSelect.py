import psycopg2


def selectConfigSystemInfo(connection, systemID):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT tblsystem.name, tblsystem.description "
                       "FROM tblsystem WHERE tblsystem.systemID = %s", (str(systemID)))
        rec = cursor.fetchall()
        cursor.close()
        return rec[0]

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


def selectAllOnlineConfigs(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT tblsystem.systemID, tblrosmonitoring.monitorID, tblconfigonline.onlineID, 'online' "
            "FROM tblsystem INNER JOIN tblrosmonitoring ON tblsystem.systemID = tblrosmonitoring.systemID "
            "INNER JOIN tblconfigonline ON  tblrosmonitoring.monitorID = tblconfigonline.monitorID")
        rec = cursor.fetchall()
        cursor.close()
        return rec

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


def selectConfigFile(connection, onlineID):
    try:
        yamlFile = ""
        cursor = connection.cursor()
        yamlFile += "nodes:\n"
        yamlFile += selectNodes(cursor, onlineID)
        yamlFile += "\n\nmonitors:\n"
        yamlFile += selectMonitors(cursor, onlineID)
        cursor.close()
        return yamlFile

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return ""


def selectNodes(cursor, onlineid):
    try:
        rtrstr = ""
        cursor.execute(
            "SELECT name, package, nodepath  FROM tblnodesonline "
            "WHERE onlineid = " + str(onlineid))
        rec = cursor.fetchall()
        for record in rec:
            rtrstr += "  - node:\n"
            rtrstr += ("      name: " + str(record[0]) + "\n")
            rtrstr += ("      package: " + record[1] + "\n")
            rtrstr += ("      path: " + record[2] + "\n")
        return rtrstr

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return ""


def selectMonitors(cursor, onlineid):
    try:
        rtrstr = ""
        cursor.execute(
            "SELECT nameid, log, silent, oracle_port, oracle_url, oracle_action, monitorsid FROM tblmonitorsonline "
            "WHERE onlineid = " + str(onlineid))
        rec = cursor.fetchall()
        for record in rec:
            rtrstr += "  - monitor:\n"
            rtrstr += ("      id: " + str(record[0]) + "\n")
            rtrstr += ("      log: " + record[1] + "\n")
            rtrstr += ("      silent: " + ('False' if str(record[2]) == '0' else 'True') + "\n")
            rtrstr += "      oracle:\n"
            rtrstr += ("        port: " + record[3] + "\n")
            rtrstr += ("        url: " + record[4] + "\n")
            rtrstr += ("        action: " + record[5] + "\n")
            rtrstr += selectTopics(cursor, record[6])

        return rtrstr

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return ""


def selectTopics(cursor, monitorid):
    try:
        rtrstr = ""
        cursor.execute(
            "SELECT type, action, topicid, name FROM tbltopicsonline "
            "WHERE monitorsid = " + str(monitorid))
        rec = cursor.fetchall()
        rtrstr += "      topics:\n"
        for record in rec:
            rtrstr += "        - name: " + record[3] + "\n"
            rtrstr += ("          type: " + str(record[0]) + "\n")
            rtrstr += ("          action: " + record[1] + "\n")
            rtrstr += selectPublishers(cursor, record[2])
        return rtrstr

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return ""


def selectPublishers(cursor, topicid):
    try:
        rtrstr = ""
        cursor.execute(
            "SELECT name FROM tblpublishersonline "
            "WHERE topicid = " + str(topicid))
        rec = cursor.fetchall()
        rtrstr += "          publishers:\n"
        for record in rec:
            rtrstr += "            - " + record[0] + "\n"
        return rtrstr

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return ""
