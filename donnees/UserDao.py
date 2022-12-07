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
                "firstname": row[2],
                "email": row[3],
                "pseudo": row[4],
                "sexe": row[5],
                "phone": row[6],
                "password": row[7],
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

def getUser(id):
    connection = database.initialiseConnection()
    cursor = connection.cursor()
    sql = "SELECT * FROM pfe.users WHERE id_user = %i" % (id)
    try:
        cursor.execute(sql)
        connection.commit()
        result = cursor.fetchone()
        user = {
            "id_user": result[0],
            "email": result[1],
            "last_name": result[2],
            "first_name": result[3],
            "password": result[4],
            "campus": result[5],
            "role": result[6]
        }
        return user
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

