from flask import abort
from werkzeug.exceptions import NotFound

import data.database as database
from models.Favorite import Favorite
import psycopg2


class FavoritesDAO:
    def __init__(self):
        pass

    def get_favorite(selfself, id_teacher, id_student):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT id_student, id_teacher FROM projet.favorites " \
              "WHERE id_student = %i AND id_teacher = %i" % (
                  id_student, id_teacher
              )
        try:
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchone()
            if result is None:
                abort(404, "Favorite not found")
            favorite = Favorite(int(result[0]), int(result[1]))
            return favorite
        except NotFound as not_found_e:
            raise not_found_e
        except (Exception, psycopg2.DatabaseError) as e:
            print("----------")
            print(type(e))
            print("----------")
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e
        finally:
            cursor.close()
            connection.close()

    def get_favorite_teachers_from_user(self, id):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT id_student, id_teacher FROM projet.favorites WHERE id_student = %i" % (id)
        results_export_fav_teachers = []
        try:
            cursor.execute(sql)
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                favorite = Favorite(int(row[0]), int(row[1]))
                results_export_fav_teachers.append(favorite)

            return results_export_fav_teachers

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

    def get_most_favorites_teachers(self):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT id_teacher, count(id_student) as total FROM projet.favorites " \
              "GROUP BY id_teacher ORDER BY total DESC"
        results_export_fav_teachers = []
        try:
            cursor.execute(sql)
            connection.commit()
            results = cursor.fetchall()

            for row in results:
                res = {
                    "id_teacher": row[0],
                    "total_like": row[1]
                }
                results_export_fav_teachers.append(res)

            return results_export_fav_teachers

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

    def add_favorite(self, favorite):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "INSERT INTO projet.favorites(id_teacher, id_student)" \
              " VALUES( %(id_teacher)s, %(id_student)s)"
        try:
            dico_variables = {
                "id_teacher": int(favorite.id_teacher),
                "id_student": int(favorite.id_student)
            }
            cursor.execute(sql, dico_variables)
            connection.commit()
            return favorite
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

    def remove_favorite(self, favorite):
        print(favorite)
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "DELETE FROM projet.favorites " \
              "WHERE id_student = '%s' AND id_teacher = '%s'" % (
                  favorite['id_student'], favorite['id_teacher']
              )

        try:
            cursor.execute(sql)
            connection.commit()
            return favorite
        except (Exception, psycopg2.DatabaseError) as e:
            print("----------")
            print(type(e))
            print("----------")
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e
        finally:
            cursor.close()
            connection.close()
