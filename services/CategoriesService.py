from flask import abort
from werkzeug.exceptions import NotFound

from data.CategoriesDAO import CategoriesDAO


class CategoriesService:
    categories_dao = CategoriesDAO()

    def __init__(self):
        pass

    def get_all_categories(self):
        return self.categories_dao.get_all_categories()
