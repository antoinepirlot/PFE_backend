import donnees.database as database
import psycopg2


def getUsers():
    connection = database.initialiseConnection()
    cursor = connection.cursor()
    sql = "SELECT * FROM projet.users"
    resultsExportUsers = []
    try:
        cursor.execute(sql)
        connection.commit()
        results = cursor.fetchall()
        for row in results:
            user = {
                "id_user": row[0],
                "lastname": row[1],
                "firstname": row[2]
            }
            resultsExportUsers.append(user)
        return resultsExportUsers
    except (Exception, psycopg2.DatabaseError) as e:
        try:
            print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
            raise Exception from e
        except IndexError:
            print("SQL Error: %s" % str(e))
            raise Exception from e
    finally:
        cursor.close()
        connection.close()

