import unittest
from unittest.mock import Mock

from app.main import app
from data.DAO.CategoriesDAO import CategoriesDAO
from data.DAO.RatingsDAO import RatingsDAO
from data.services.DALService import DALService


class RatingsTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.ratings_dao = RatingsDAO()
        self.dal_service = DALService()
        self.dal_service.start = Mock()
        self.dal_service.commit_transaction = Mock()
        self.dal_service.rollback_transaction = Mock()
        self.rating_json = {
            "id_rater": 1,
            "id_rated": -1,
            "rating_text": "bof comme prof j'ai pas vrmt apprécié",
            "rating_number": 3
        }

    def test_create_rating_negative_id_teacher(self):
        self.dal_service.execute = Mock()
        response = self.app.post('/ratings/', data=self.rating_json)
        self.assertEqual(400, response.status_code)


if __name__ == '__main__':
    unittest.main()
