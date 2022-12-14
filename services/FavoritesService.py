from Exceptions.WebExceptions.ConflictException import ConflictException
from Exceptions.WebExceptions.NotFoundException import NotFoundException
from data.DAO.FavoritesDAO import FavoritesDAO
from data.services.DALService import DALService


class FavoritesService:

    def __init__(self):

        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of FavoritesService class, a new one is created
            cls._dal_service = DALService()
            cls._favorites_DAO = FavoritesDAO()
            cls._instance = super(FavoritesService, cls).__new__(cls)
        # There's already an instance of FavoritesService class, so the existing one is returned
        return cls._instance

    def get_favorite(self, id_teacher, id_student):
        """
        Get the favorite retrieved by its id_teacher and id_student
        :param id_teacher: the id of the teacher
        :param id_student: the id of the student
        :return: the favorite or notfoundexception
        """
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
        """
        Get all favorites from a specific user
        :param id: the id of the user
        :return: list of all his favorite
        """
        try:
            self._dal_service.start()
            results = self._favorites_DAO.get_favorite_teachers_from_user(id)
            if results is None:
                raise NotFoundException
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e

    def get_most_favorites_teachers(self):
        """
        Get a list with the id teacher and its number of favorites student gives to him foreach teacher
        :return: list with the id teacher and its number of favorites student gives to him foreach teacher
        """
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
        """
        Create a favorite
        :param favorite: the favorite we want to add
        :return: the created favorite
        """
        try:
            self._dal_service.start()
            result = self._favorites_DAO.get_favorite(favorite.id_teacher, favorite.id_student)
            if result is not None:
                raise ConflictException("You already like this profile")
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
        """
        Remove a favorite
        :param id_teacher: the id of the teacher
        :param id_student: the id of the student
        """
        try:
            self._dal_service.start()
            self._favorites_DAO.remove_favorite(id_teacher, id_student)
            self._dal_service.commit_transaction()
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e
