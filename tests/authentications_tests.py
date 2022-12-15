import unittest
from unittest.mock import Mock

import bcrypt

from utils_for_tests import get_good_token
from app.main import app
from data.DAO.UsersDAO import UsersDAO
from data.services.DALService import DALService


class AuthenticationsTests(unittest.TestCase):
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

    def test_login_with_empty_password(self):
        response = self.app.post("authentications/login", json={"email": "a@gmail.com",
                                                                "password": ""})
        self.assertEqual(400, response.status_code)

    def test_login_with_empty_email(self):
        response = self.app.post("authentications/login", json={"email": "",
                                                                "password": "hard_password"})
        self.assertEqual(400, response.status_code)

    def test_login_wrong_password(self):
        self.dal_service.execute = Mock(return_value=self.user_from_db)
        response = self.app.post("authentications/login", json={"email": "requinFR@gmail.com",
                                                                "password": "wrong_password"})
        self.assertEqual(404, response.status_code)



if __name__ == '__main__':
    unittest.main()
