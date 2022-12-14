import unittest
from unittest.mock import Mock

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


if __name__ == '__main__':
    unittest.main()
