import psycopg2


def runQuery(connection, query):
    try:
        print("Executing the query...")
        cursor = connection.cursor()
        cursor.execute(query)
        rec = cursor.fetchall()
        cursor.close()
        print("Query executed.")
        return rec
    except(Exception, psycopg2.Error) as errorMsg:
        print("A database-related error occured: ", errorMsg)
        return []


def printTable(table):
    print('\nResult Table: \n')
    for row in table:
        print(row)
