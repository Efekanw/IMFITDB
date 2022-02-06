import psycopg2


class onlineConfigfile:
    def __init__(self):
        self.nodeList = []
        self.monitorList = []

    class node:
        def __init__(self):
            self.name = ""
            self.package = ""
            self.path = ""

    class monitor:
        def __init__(self):
            self.id = ""
            self.log = ""
            self.silent = ""
            self.oraclePort = ""
            self.oracleUrl = ""
            self.oracleAction = ""
            self.topicList = []

        class topic:
            def __init__(self):
                self.name = ""
                self.type = ""
                self.action = ""
                self.publisherList = []


def insertConfigFile(connection, filename, monitorID):
    f = open(filename, 'r')
    cFile = onlineConfigfile()
    line = f.readline()
    while line:
        line = line.strip()
        if line[:7] == "- node:":
            node = onlineConfigfile.node()
            node.name = (f.readline().replace(' ', '').replace("name:", "")).split("#")[0].rstrip("\n")
            node.package = (f.readline().replace(' ', '').replace("package:", "")).split("#")[0].rstrip("\n")
            node.path = (f.readline().replace(' ', '').replace("path:", "")).split("#")[0].rstrip("\n")
            cFile.nodeList.append(node)
        if line[:9] == "monitors:":
            break
        line = f.readline()
    while line:
        if line[:9] == "monitors:":
            monitor = onlineConfigfile().monitor()
            (f.readline())
            monitor.id = (f.readline().replace(' ', '').replace("id:", "")).split("#")[0].rstrip("\n")
            monitor.log = (f.readline().replace(' ', '').replace("log:", "")).split("#")[0].rstrip("\n")
            monitor.silent = (f.readline().replace(' ', '').replace("silent:", "")).split("#")[0].rstrip("\n")
            (f.readline())
            monitor.oraclePort = (f.readline().replace(' ', '').replace("port:", "")).split("#")[0].rstrip("\n")
            monitor.oracleUrl = (f.readline().replace(' ', '').replace("url:", "")).split("#")[0].rstrip("\n")
            monitor.oracleAction = (f.readline().replace(' ', '').replace("action:", "")).split("#")[0].rstrip("\n")
            while line:
                line = line.strip()
                if line[:7] == "- name:": #topic
                    topic=onlineConfigfile.monitor.topic()
                    topic.name = (line.replace(' ', '').replace("-name:", "")).split("#")[0].rstrip("\n")
                    topic.type = (f.readline().replace(' ', '').replace("type:", "")).split("#")[0].rstrip("\n")
                    topic.action = (f.readline().replace(' ', '').replace("action:", "")).split("#")[0].rstrip("\n")
                    f.readline()
                    subLine = f.readline()
                    while subLine:
                        if subLine[:14] != "            - ":
                            break
                        subLine = (subLine.replace(' ', '').replace("-", "")).split("#")[0].rstrip("\n")
                        topic.publisherList.append(subLine)
                        subLine = f.readline()
                    monitor.topicList.append(topic)
                line = f.readline()
            cFile.monitorList.append(monitor)
        line = f.readline()
    insert2db(connection, cFile, monitorID)


def insert2db(connection, configClass, monitorID):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tblconfigonline(monitorID)"
            "VALUES(%s) RETURNING onlineID;", (str(monitorID)))
        onlineID = cursor.fetchall()[0][0]
        for node in configClass.nodeList:
            cursor.execute(
                "INSERT INTO tblnodesonline(name, package, nodepath, onlineid)"
                "VALUES(%s, %s, %s, %s)",
                (node.name, node.package, node.path, str(onlineID))
            )
        for monitor in configClass.monitorList:
            cursor.execute(
                "INSERT INTO tblmonitorsonline(nameid, log, silent, oracle_port, oracle_url, oracle_action, onlineid)"
                "VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING monitorsID;",
                (monitor.id, monitor.log, str(0 if monitor.silent == "0" else 1), monitor.oraclePort, monitor.oracleUrl,
                 monitor.oracleAction, str(onlineID))
            )
            monitorsID = cursor.fetchall()[0][0]
            for topic in monitor.topicList:
                cursor.execute(
                    "INSERT INTO tbltopicsonline(name, type, action, monitorsID)"
                    "VALUES(%s, %s, %s, %s) RETURNING topicID;",
                    (topic.name, topic.type, topic.action, str(monitorsID))
                )
                topicID = cursor.fetchall()[0][0]
                for publisher in topic.publisherList:
                    cursor.execute(
                        "INSERT INTO tblpublishersonline(name, topicID)"
                        "VALUES(%s, %s)",
                        (publisher, str(topicID))
                    )
        connection.commit()
        cursor.close()

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
