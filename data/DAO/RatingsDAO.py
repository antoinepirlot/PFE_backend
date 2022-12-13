import psycopg2

from Exceptions.FatalException import FatalException
from data.services.DALService import DALService
from models.Rating import Rating


class RatingsDAO:
    def __init__(self):
        self.dal = DALService()

    def create_one_rating(self, rating):
        """
        Create a rating in the database.
        :param: rating: the rating to add
        :return: the rating added.
        """
        sql = """
                       INSERT INTO projet.ratings(rating_text, rating_number, id_rater, id_rated) 
                       VALUES( %(rating_text)s, %(rating_number)s, %(id_rater)s, %(id_rated)s)
                     """
        try:
            dico_variables = {"rating_text": str(rating.rating_text), "rating_number": int(rating.rating_number),
                              "id_rater": int(rating.id_rater),
                              "id_rated": int(rating.id_rated)
                              }
            self.dal.execute(sql, dico_variables)
            return rating
        except (Exception, psycopg2.DatabaseError) as e:
            raise FatalException

    def get_rating_by_id_rater_and_id_rated(self, id_rater, id_rated):
        """
        Get rating by the rater and the rated id.
        :param: id_rater: the user's id that rated
        :param: id_rated: the user's id that gets a rating
        :return: the rating, If there's no rating, it returns None
        """
        sql = "SELECT id_rater, id_rated, rating_text, rating_number FROM projet.ratings " \
              "WHERE id_rater = %(id_rater)s AND id_rated = %(id_rated)s"
        try:
            result = self.dal.execute(sql, {"id_rater": id_rater, "id_rated": id_rated}, True)
            if len(result) == 0:
                return None
            result = result[0]
            rating = Rating(int(result[0]), int(result[1]), str(result[2]), int(result[3]))
            return rating
        except (Exception, psycopg2.DatabaseError) as e:
            raise FatalException

    def get_ratings_from_teacher(self, id_teacher):
        """
        Get rating by the rated id (teacher).
        :param: id_teacher: the user's id that gets a rating
        :return: list of ratings, If there's no ratings, it returns None
        """

        sql = "SELECT id_rater, id_rated, rating_text, rating_number FROM projet.ratings WHERE id_rated = %(id_teacher)s "

        results = self.dal.execute(sql, {"id_teacher": id_teacher}, True)
        all_ratings = []
        for row in results:
            rating = Rating(int(row[0]), int(row[1]), str(row[2]), int(row[3]))
            all_ratings.append(rating)
        return all_ratings

