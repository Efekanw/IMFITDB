import psycopg2


def selectAllOfflineConfigs(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT tblsystem.systemID, tblrosmonitoring.monitorID, tblconfigoffline.offlineID, 'offline' "
            "FROM tblsystem INNER JOIN tblrosmonitoring ON tblsystem.systemID = tblrosmonitoring.systemID "
            "INNER JOIN tblconfigoffline ON  tblrosmonitoring.monitorID = tblconfigoffline.monitorID")
        rec = cursor.fetchall()
        return rec

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


def selectConfigFile(connection, offline_id):
    try:
        yaml_file = ""
        cursor = connection.cursor()
        yaml_file += "\nmonitors:\n"
        yaml_file += selectMonitors(cursor, offline_id)
        cursor.close()
        return yaml_file

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return ""


def selectMonitors(cursor, offlineId):
    try:
        rtr_str = ""
        cursor.execute(
            "SELECT nameId, log, silent, monitorId FROM tblMonitorsOffline "
            "WHERE offlineId = " + str(offlineId))
        rec = cursor.fetchall()
        for record in rec:
            rtr_str += "  - monitor:\n"
            rtr_str += ("      id: " + str(record[0]) + "\n")
            rtr_str += ("      log: " + record[1] + "\n")
            rtr_str += ("      silent: " + ('False' if str(record[2]) == '0' else 'True') + "\n")
            rtr_str += selectTopics(cursor, record[3])
        return rtr_str

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return ""


def selectTopics(cursor, monitorId):
    try:
        rtr_str = ""
        cursor.execute(
            "SELECT type, action, name FROM tblTopicsOffline "
            "WHERE monitorId = " + str(monitorId))
        rec = cursor.fetchall()
        rtr_str += "      topics:\n"
        for record in rec:
            rtr_str += "        - name: " + record[2] + "\n"
            rtr_str += ("          type: " + str(record[0]) + "\n")
            rtr_str += ("          action: " + record[1] + "\n")
        return rtr_str

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return ""



