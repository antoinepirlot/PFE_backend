from flask import abort
from werkzeug.exceptions import NotFound

from data.CategoriesDAO import CategoriesDAO
from data.services.DALService import DALService


class CategoriesService:
    categories_dao = CategoriesDAO()

    def __init__(self):
        self.dal = DALService()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            # No instance of CategoriesService class, a new one is created
            cls.instance = super(CategoriesService, cls).__new__(cls)
        # There's already an instance of CategoriesService class, so the existing one is returned
        return cls.instance

    def get_all_categories(self):
        self.dal.start()
        try:
            all_categories = self.categories_dao.get_all_categories()
            self.dal.commit_transaction()
            return all_categories
        except Exception as e:
            self.dal.rollback_transaction()
            raise e
