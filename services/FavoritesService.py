from flask import abort

from data.DAO.FavoritesDAO import FavoritesDAO
from data.services.DALService import DALService


class FavoritesService:

    def __init__(self):
        self._favorites_DAO = FavoritesDAO()
        self._dal_service = DALService()

    def get_favorite(self, id_teacher, id_student):
        try:
            self._dal_service.start()
            results = self._favorites_DAO.get_favorite(id_teacher, id_student)
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()

    def get_favorites_from_user(self, id):
        try:
            self._dal_service.start()
            results = self._favorites_DAO.get_favorite_teachers_from_user(id)
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()

    def get_most_favorites_teachers(self):
        try:
            self._dal_service.start()
            results = self._favorites_DAO.get_most_favorites_teachers()
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()

    def add_favorite(self, favorite):
        try:
            self._dal_service.start()
            # TODO use unique constraint database to check this
            self._favorites_DAO.get_favorite(favorite.id_teacher, favorite.id_student)
            self._dal_service.commit_transaction()
            # TODO same as ChatRooms
            abort(409, "You already have this teacher in your favorites.")
        except Exception as not_found_p:
            self._dal_service.rollback_transaction()
            try:
                self._dal_service.start()
                favorite = self._favorites_DAO.add_favorite(favorite)
                self._dal_service.commit_transaction()
                return favorite
            except Exception as e:
                self._dal_service.rollback_transaction()
        # TODO Proposed code:
        # try:
        #     self._dal_service.start()
        #     results = self._favorites_DAO.add_favorite(favorite)
        #     self._dal_service.commit_transaction()
        #     return results
        # except Exception as e:
        #     # TODO here there's an exception while creating favorite (as syntax as unique error) (sorry for my poor english haha)
        #     self._dal_service.rollback_transaction()

    def remove_favorite(self, favorite):
        try:
            self._dal_service.start()
            results = self._favorites_DAO.remove_favorite(favorite)
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()
