from data.RatingsDAO import RatingsDAO
from data.UsersDao import UsersDAO


class RatingsService:
    ratings_DAO = RatingsDAO()
    users_DAO = UsersDAO()

    def __init__(self):
        pass

    def get_ratings(self, id_teacher):
        return self.ratings_DAO.get_ratings_from_teacher(id_teacher)

    def create_rating(self, rating):
        self.users_DAO.getUserById(rating.id_rater)
        self.users_DAO.getUserById(rating.id_rated)
        #TODO : check if a finish appointment exist
        return rating

