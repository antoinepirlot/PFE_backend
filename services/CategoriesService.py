from data.DAO.CategoriesDAO import CategoriesDAO
from data.services.DALService import DALService


class CategoriesService:

    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of CategoriesService class, a new one is created
            cls._dal = DALService()
            cls._categories_dao = CategoriesDAO()
            cls._instance = super(CategoriesService, cls).__new__(cls)
        # There's already an instance of CategoriesService class, so the existing one is returned
        return cls._instance

    def get_all_categories(self):
        """
        Get all categories
        :return: all categories
        """
        try:
            self._dal.start()
            all_categories = self._categories_dao.get_all_categories()
            self._dal.commit_transaction()
            return all_categories
        except Exception as e:
            self._dal.rollback_transaction()
            raise e
