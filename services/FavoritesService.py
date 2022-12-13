from Exceptions.WebExceptions.NotFoundException import NotFoundException
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
            if results is None:
                raise NotFoundException("Favorite not found")
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e

    def get_favorites_from_user(self, id):
        try:
            self._dal_service.start()
            results = self._favorites_DAO.get_favorite_teachers_from_user(id)
            print("results ", results)
            if results is None:
                raise NotFoundException
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e

    def get_most_favorites_teachers(self):
        try:
            self._dal_service.start()
            results = self._favorites_DAO.get_most_favorites_teachers()
            if results is None:
                raise NotFoundException
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e

    def add_favorite(self, favorite):
        try:
            self._dal_service.start()
            result = self._favorites_DAO.add_favorite(favorite)
            self._dal_service.commit_transaction()
            return result
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e
        # TODO Proposed code:
        # try:
        #     self._dal_service.start()
        #     results = self._favorites_DAO.add_favorite(favorite)
        #     self._dal_service.commit_transaction()
        #     return results
        # except Exception as e:
        #     # TODO here there's an exception while creating favorite (as syntax as unique error) (sorry for my poor english haha)
        #     self._dal_service.rollback_transaction()

    def remove_favorite(self, id_teacher, id_student):
        try:
            self._dal_service.start()
            results = self._favorites_DAO.remove_favorite(id_teacher, id_student)
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e
