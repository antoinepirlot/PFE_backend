import unittest
from unittest.mock import Mock

from app.main import app
from data.DAO.UsersDAO import UsersDAO
from data.services.DALService import DALService
from models.User import User


class UsersTests(unittest.TestCase):
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
        self.all_users_from_db = [
            (1,
             'Dupont',
             'Pierre',
             'requinFR@gmail.com',
             'REQUIN',
             'male',
             '(+32)4 77 123 659',
             '$2b$12$GywdfXS27bA0BrZFgZrbW.m9vqCT28SBjek.3eQF/K3AyMD7ZvnCO'),
            (2,
             'Griezi',
             'Pablo',
             'picpic@gmail.com',
             'pab',
             'male',
             '(+32)4 77 143 659',
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
        self.user2_json = {
            "email": "picpic@gmail.com",
            "firstname": "Pablo",
            "id_user": 2,
            "lastname": "Griezi",
            "password": "$2b$12$GywdfXS27bA0BrZFgZrbW.m9vqCT28SBjek.3eQF/K3AyMD7ZvnCO",
            "phone": "(+32)4 77 143 659",
            "pseudo": "pab",
            "sexe": "male"
        }
        self.new_user = {
             "lastname": "Feuille",
              "firstname": "Jean",
              "email": "a256@gmail.com",
              "pseudo": "a256",
              "sexe": "male",
              "phone": "0477555978",
              "password": "a256"
        }

    def test_user_by_email_ok(self):
        self.dal_service.execute = Mock(return_value=self.user_from_db)
        response = self.app.get('/users/requinFR@gmail.com')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.user_json, response.get_json())

    def test_user_by_email_non_existing_email(self):
        self.dal_service.execute = Mock(return_value=[])
        response = self.app.get('/users/noexists@gmail.com')
        self.assertEqual(404, response.status_code)

    def test_get_user_by_id_ok(self):
        self.dal_service.execute = Mock(return_value=self.user_from_db)
        response = self.app.get('/users/idUser=1')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.user_json, response.get_json())

    def test_get_user_by_id_non_exisiting_id(self):
        self.dal_service.execute = Mock(return_value=[])
        response = self.app.get('/users/idUser=100')
        self.assertEqual(404, response.status_code)

    def test_get_users_ok(self):
        self.dal_service.execute = Mock(return_value=self.all_users_from_db)
        response = self.app.get('/users')
        self.assertEqual(200, response.status_code)
        self.assertEqual([self.user_json, self.user2_json], response.get_json())

    def test_get_users_by_pseudo_ok(self):
        self.dal_service.execute = Mock(return_value=self.user_from_db)
        response = self.app.get('/users/pseudo/REQUIN')
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.user_json, response.get_json())

    def test_get_users_by_pseudo_non_existing_pseudo(self):
        self.dal_service.execute = Mock(return_value=[])
        response = self.app.get('/users/pseudo/RENARD_FUTE')
        self.assertEqual(404, response.status_code)

    def test_add_users_ok(self):
        self.dal_service.execute = Mock(side_effect=[[], [], []])
        response = self.app.post('/users', json=self.new_user)
        self.assertEqual(201, response.status_code)

    def test_add_users_with_pseudo_already_taken(self):
        user_json_paola = {
            "email": "pieuvre@gmail.com",
            "firstname": "Paola",
            "id_user": 15,
            "lastname": "Richi",
            "password": "$2b$12$GywdfXS27bA0BrZFgZrbW.m9vqCT28SBjek.3eQF/K3AyMD7ZvnCO",
            "phone": "(+32)4 15 123 659",
            "pseudo": "REQUIN",
            "sexe": "female"
        }
        self.dal_service.execute = Mock(side_effect=[[], self.user_from_db])
        response = self.app.post('/users', json=user_json_paola)
        self.assertEqual(409, response.status_code)


if __name__ == '__main__':
    unittest.main()
