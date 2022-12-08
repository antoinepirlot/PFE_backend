import data.database as database
import models.User as User
import psycopg2


class FavoritesDAO:

    def getFavTeachersFromUser(self, id):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT id_student, id_teacher FROM projet.favorites WHERE id_student = %i" % (id)
        resultsExportFavTeachers = []
        try:
            cursor.execute(sql)
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                favorite = {
                    "id_user": row[0],
                    "id_teacher": row[1],
                }
                resultsExportFavTeachers.append(favorite)

            return resultsExportFavTeachers

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

    def addFavorite(self, favorite):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "INSERT INTO projet.favorites VALUES('%s', '%s')" % (
            favorite['id_teacher'], favorite['id_student']
        )
        try:
            cursor.execute(sql)
            connection.commit()
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