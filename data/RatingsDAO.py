from flask import abort
from werkzeug.exceptions import NotFound

import data.database as database
from models.Rating import Rating
import psycopg2


class RatingsDAO:
    def __init__(self):
        pass

    def get_rating_by_id_rater_and_id_rated(self, id_rater, id_rated):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT id_rater, id_rated, rating_text, rating_number FROM projet.ratings " \
              "WHERE id_rater = %(id_rater)s AND id_rated = %(id_rated)s"
        try:
            cursor.execute(sql, {"id_rater": id_rater, "id_rated": id_rated})
            connection.commit()
            result = cursor.fetchone()
            if result is None:
                abort(404, "Rating not found")
            rating = Rating(int(result[0]), int(result[1]), str(result[2]), int(result[3]))
            return rating
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

    def get_ratings_from_teacher(self, id_teacher):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT id_rater, id_rated, rating_text, rating_number FROM projet.ratings WHERE id_rated = %(id_teacher)s "

        try:
            cursor.execute(sql, {"id_teacher": id_teacher})
            connection.commit()
            results = cursor.fetchall()
            all_ratings = []
            for row in results:
                rating = Rating(int(row[0]), int(row[1]), str(row[2]), int(row[3]))
                all_ratings.append(rating)
            return all_ratings
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
