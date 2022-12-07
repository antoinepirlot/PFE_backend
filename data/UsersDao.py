import data.database as database
import psycopg2


class UsersDAO:
    def getUsers(self):
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

    def getUserById(self, id):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT * FROM projet.users WHERE id_user = %i" % (id)
        try:
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchone()
            user = {
                "id_user": result[0],
                "lastname": result[1],
                "firstname": result[2],
                "email": result[3],
                "pseudo": result[4],
                "sexe": result[5],
                "phone": result[6],
                "password": result[7],
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

    def singInUser(self, user):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "INSERT INTO projet.users VALUES (DEFAULT,'%s','%s','%s','%s','%s','%s','%s')" % (
            user['lastname'], user['firstname'], user['email'], user['pseudo'], user['sexe'], user['phone'],
            user['password'])
        try:
            cursor.execute(sql)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                connection.rollback()
                print("SQL Error: %s" % str(e))
                raise Exception from e
        finally:
            cursor.close()
            connection.close()
