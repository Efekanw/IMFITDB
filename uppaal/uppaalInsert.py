from datetime import datetime
import re
import xml.etree.ElementTree as ET

def insertXmlFile(connection, filename, systemID, description):
    cursor = connection.cursor()
    f = open(filename, "r")
    xmlFile = f.read()

    cursor.execute(
        "INSERT INTO tblUppaal(createDate, description, xmlfile, systemID)"
        "VALUES(%s, %s, %s, %s) RETURNING modelID;",
        (str(datetime.now()), description, xmlFile, systemID))

    modelID = cursor.fetchall()[0][0]

    xmlFile = xmlFile.replace('\n', '')
    pattern = "<queries>(.*)</queries>"
    chopped = re.search(pattern, xmlFile)
    
    if chopped:
        xmlFile = "<queries> " + chopped.group(1) + " </queries>"

        tree = ET.ElementTree(ET.fromstring(xmlFile))
        root = tree.getroot()

        for query in root.findall('query'):
            cursor.execute(
                     "INSERT INTO tblQuery(modelID, query, description)"
                     "VALUES(%s, %s, %s)",
                     (modelID, query[0].text, query[1].text))

    connection.commit()
    cursor.close()
