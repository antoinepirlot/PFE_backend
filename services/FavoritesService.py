from flask import abort
from werkzeug.exceptions import NotFound

from data.FavoritesDAO import FavoritesDAO


class FavoritesService:
    favorites_DAO = FavoritesDAO()

    def __init__(self):
        pass

    def get_favorite(self, id_teacher, id_student):
        return self.favorites_DAO.get_favorite(id_teacher, id_student)

    def get_favorites_from_user(self, id):
        return self.favorites_DAO.get_favorite_teachers_from_user(id)

    def get_most_favorites_teachers(self):
        return self.favorites_DAO.get_most_favorites_teachers()

    def add_favorite(self, favorite):
        if favorite.id_teacher == favorite.id_student:
            abort(412, "You cannot add yourself to your favorites")
        try:
            self.favorites_DAO.get_favorite(favorite.id_teacher, favorite.id_student)
            abort(409, "You already have this teacher on your favorite.")
        except NotFound as not_found_p:
            favorite = self.favorites_DAO.add_favorite(favorite)

        return favorite

    def remove_favorite(self, favorite):
        return self.favorites_DAO.remove_favorite(favorite)
