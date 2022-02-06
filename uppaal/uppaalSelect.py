
def selectUppaalQueries(connection, modelID):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT tblquery.query, tblquery.description, tblquery.result FROM tblquery WHERE tblquery.modelID=%s", str(modelID))
    rec = cursor.fetchall()
    cursor.close()
    return rec

def selectUppaalModelInfo(connection, systemID):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT systemID, modelID, createDate, description, xmlFile  FROM tblUppaal "
        "WHERE systemId = %s",
        (str(systemID)))
    rec = cursor.fetchall()
    cursor.close()
    return rec[0]

def getAllUppaalRecords(connection):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT tblSystem.systemID, tblSystem.name FROM tblSystem INNER JOIN tblUppaal ON tblSystem.systemID = tblUppaal.systemID")
    rec = cursor.fetchall()
    cursor.close()
    return rec

def selectUppaalModelXml(connection, systemID):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT xmlFile  FROM tblUppaal "
        "WHERE systemId = %s",
        (str(systemID)))
    rec = cursor.fetchall()
    cursor.close()
    return rec[0][0]
