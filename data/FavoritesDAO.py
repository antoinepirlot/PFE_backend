import psycopg2
from flask import abort
from werkzeug.exceptions import NotFound

from data.services.DALService import DALService
from models.Favorite import Favorite


class FavoritesDAO:
    def __init__(self):
        self._dal_service = DALService()

    def get_favorite(self, id_teacher, id_student):
        sql = """
            SELECT id_student, id_teacher FROM projet.favorites 
            WHERE id_student = %(id_student)s AND id_teacher = %(id_teacher)s
        """
        values = {"id_student": id_student, "id_teacher": id_teacher}
        try:
            result = self._dal_service.execute(sql, values, True)
            if len(result) == 0:
                # TODO abort in routes
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

    def get_favorite_teachers_from_user(self, id_student):
        sql = """
            SELECT id_student, id_teacher 
            FROM projet.favorites 
            WHERE id_student = %(id_student)s
        """
        values = {"id_student": id_student}
        results_export_fav_teachers = []
        try:
            results = self._dal_service.execute(sql, values, True)
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

    def get_most_favorites_teachers(self):
        sql = """
            SELECT id_teacher, count(id_student) as total FROM projet.favorites 
            GROUP BY id_teacher ORDER BY total DESC
        """
        results_export_fav_teachers = []
        try:
            results = self._dal_service.execute(sql, [], True)
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

    def add_favorite(self, favorite):
        sql = """
            INSERT INTO projet.favorites(id_teacher, id_student)
            VALUES( %(id_teacher)s, %(id_student)s)
            RETURNING id_teacher, id_student
        """
        values = {"id_teacher": int(favorite.id_teacher), "id_student": int(favorite.id_student)}
        try:
            result = self._dal_service.execute(sql, values, True)[0]
            return Favorite(result[0], result[1])
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e

    def remove_favorite(self, favorite):
        sql = """
            DELETE FROM projet.favorites 
            WHERE id_student = %(id_student)s AND id_teacher = %(id_teacher)s
        """
        values = {"id_student": favorite.id_student, "id_teacher": favorite.id_teacher}
        try:
            return self._dal_service.execute(sql, values, True)
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
