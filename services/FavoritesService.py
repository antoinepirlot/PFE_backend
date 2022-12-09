from data.FavoritesDAO import FavoritesDAO


class FavoritesService:
    favorites_DAO = FavoritesDAO()

    def __init__(self):
        pass

    def get_favorites_from_user(self, id):
        return self.favorites_DAO.getFavTeachersFromUser(id)

    def add_favorite(self, favorite):
        return self.favorites_DAO.addFavorite(favorite)