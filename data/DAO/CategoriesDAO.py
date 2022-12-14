import psycopg2

from data.services.DALService import DALService
from models.Category import Category


class CategoriesDAO:
    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of CategoriesDAO class, a new one is created
            cls._dal = DALService()
            cls._instance = super(CategoriesDAO, cls).__new__(cls)
        # There's already an instance of CategoriesDAO class, so the existing one is returned
        return cls._instance

    def get_all_categories(self):
        '''
        Get all categories
        :return: all categories
        '''
        sql = "SELECT id_category, name FROM projet.categories "
        results = self._dal.execute(sql, None, True)
        all_categories = []
        for row in results:
            rating = Category(int(row[0]), str(row[1]))
            all_categories.append(rating)
        return all_categories

    def get_all_skills_categories(self, id_user):
        '''
        Get all categories where the user with the id_user have skill
        :param id_user: the id of the user
        :return: all categories where the user have a skill
        '''
        sql = "SELECT c.id_category, c.name FROM projet.categories c, projet.teacher_skills ts, projet.users u " \
              "WHERE c.id_category = ts.id_category AND ts.id_teacher = u.id_user AND u.id_user = %(id_user)s"
        value = {"id_user": id_user}
        results = self._dal.execute(sql, value, True)
        all_categories = []
        for row in results:
            rating = Category(int(row[0]), str(row[1]))
            all_categories.append(rating)
        return all_categories
