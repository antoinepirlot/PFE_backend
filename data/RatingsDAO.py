import data.database as database
from models.Rating import Rating
import psycopg2


class RatingsDAO:
    def __init__(self):
        pass

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
