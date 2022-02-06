import psycopg2


def selectProperties(connection, monitorID):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT description, language, propertycode, propertresult FROM tblProperty WHERE monitorID = %s", (str(monitorID)))
        rec = cursor.fetchall()
        cursor.close()
        return rec

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


def insertProperty(connection, description, language, propertycode, propertresult, monitorID):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tblProperty(description, language, propertycode, propertresult, monitorid) "
                       "VALUES(%s, %s, %s, %s, %s)",
                       (description, language, propertycode, propertresult, str(monitorID)))
        connection.commit()
        cursor.close()

    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
