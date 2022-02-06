import psycopg2


class offlineConfigfile:
    def __init__(self):
        self.monitorList = []

    class monitor:
        def __init__(self):
            self.id = ""
            self.log = ""
            self.silent = False
            self.topicList = []

        class topic:
            def __init__(self):
                self.name = ""
                self.type = ""
                self.action = ""


def insertConfigFile(connection, filename, monitorid):
    f = open(filename, 'r')
    cFile = offlineConfigfile()
    line = f.readline()
    while line:
        if line[:9] == "monitors:":
            monitor = offlineConfigfile().monitor()
            (f.readline())
            monitor.id = (f.readline().replace(' ', '').replace("id:", "")).split("#")[0].rstrip("\n")
            monitor.log = (f.readline().replace(' ', '').replace("log:", "")).split("#")[0].rstrip("\n")
            monitor.silent = (f.readline().replace(' ', '').replace("silent:", "")).split("#")[0].rstrip("\n")
            (f.readline())
            while line:
                line = line.strip()
                if line[:7] == "- name:": #topic
                    topic = offlineConfigfile.monitor.topic()
                    topic.name = (line.replace(' ', '').replace("-name:", "")).split("#")[0].rstrip("\n")
                    topic.type = (f.readline().replace(' ', '').replace("type:", "")).split("#")[0].rstrip("\n")
                    topic.action = (f.readline().replace(' ', '').replace("action:", "")).split("#")[0].rstrip("\n")
                    monitor.topicList.append(topic)
                line = f.readline()
            cFile.monitorList.append(monitor)
        line = f.readline()
    insert2db(connection, cFile, monitorid)


def insert2db(connection, configClass, monitorid):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tblConfigOffline(monitorID)"
            "VALUES(%s) RETURNING offlineID;", (str(monitorid)))
        offlineID = cursor.fetchall()[0][0]
        for monitor in configClass.monitorList:
            cursor.execute(
                "INSERT INTO tblMonitorsOffline(nameid, log, silent, offlineid)"
                "VALUES(%s, %s, %s, %s) RETURNING monitorid;",
                (monitor.id, monitor.log, str(0 if monitor.silent else 1), str(offlineID))
            )
            monitorsID = cursor.fetchall()[0][0]
            for topic in monitor.topicList:
                cursor.execute(
                    "INSERT INTO tblTopicsOffline(name, type, action, monitorid)"
                    "VALUES(%s, %s, %s, %s)",
                    (topic.name, topic.type, topic.action, str(monitorsID))
                )
        connection.commit()
        cursor.close()

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
