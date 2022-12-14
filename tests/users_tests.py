import unittest
from unittest.mock import Mock

from app.main import app
from data.DAO.UsersDAO import UsersDAO
from data.services.DALService import DALService


class RatingsTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.users_dao = UsersDAO()
        self.dal_service = DALService()
        self.dal_service.start = Mock()
        self.dal_service.commit_transaction = Mock()
        self.dal_service.rollback_transaction = Mock()
        self.user_from_db = [
            (1,
             'Dupont',
             'Pierre',
             'requinFR@gmail.com',
             'REQUIN',
             'male',
             '(+32)4 77 123 659',
             '$2b$12$GywdfXS27bA0BrZFgZrbW.m9vqCT28SBjek.3eQF/K3AyMD7ZvnCO')
        ]
        self.user_json = {
            "email": "requinFR@gmail.com",
            "firstname": "Pierre",
            "id_user": 1,
            "lastname": "Dupont",
            "password": "$2b$12$GywdfXS27bA0BrZFgZrbW.m9vqCT28SBjek.3eQF/K3AyMD7ZvnCO",
            "phone": "(+32)4 77 123 659",
            "pseudo": "REQUIN",
            "sexe": "male"
        }

    def test_user_by_email(self):
        self.dal_service.execute = Mock(return_value=self.user_from_db)
        response = self.app.get('/users/requinFR@gmail.com')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.user_json, response.get_json())


if __name__ == '__main__':
    unittest.main()
