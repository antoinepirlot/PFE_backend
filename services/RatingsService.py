from data.RatingsDAO import RatingsDAO


class RatingsService:
    ratings_DAO = RatingsDAO()

    def __init__(self):
        pass

    def get_ratings(self, id_teacher):
        return self.ratings_DAO.get_ratings_from_teacher(id_teacher)
