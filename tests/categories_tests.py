import unittest
from unittest.mock import Mock
from data.CategoriesDAO import CategoriesDAO
from models.Category import Category
from app.main import app


class CategoriesTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.categories_dao = CategoriesDAO()
        self.categories_from_db = [
            Category(1,"Anglais"),
            Category(2, "Math")
        ]
        self.categories_from_db_json = [
            {
                "id_category": 1,
                "name": "Anglais"
            },
            {
                "id_category": 2,
                "name": "Math"
            }
        ]

    def test_get_all_categories(self):
        self.categories_dao.get_all_categories = Mock(return_value=self.categories_from_db)
        response = self.app.get('/categories/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.categories_from_db_json, response.get_json())


if __name__ == '__main__':
    unittest.main()
