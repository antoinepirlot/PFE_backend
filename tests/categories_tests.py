import unittest
from unittest.mock import Mock
from data.CategoriesDAO import CategoriesDAO
from data.services.DALService import DALService
from models.Category import Category
from app.main import app


class CategoriesTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.categories_dao = CategoriesDAO()
        self.dal_service = DALService()
        self.dal_service.start = Mock()
        self.dal_service.commit_transaction = Mock()
        self.dal_service.rollback_transaction = Mock()
        self.categories_from_db = [
            (
                1,
                "Anglais"
            ),
            (
                2,
                "Math"
            )
        ]
        self.categories_json = [{'id_category': 1, 'name': 'Anglais'}, {'id_category': 2, 'name': 'Math'}]

    def test_get_all_categories(self):
        self.dal_service.execute = Mock(return_value=self.categories_from_db)
        response = self.app.get('/categories/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.categories_json, response.get_json())


if __name__ == '__main__':
    unittest.main()
