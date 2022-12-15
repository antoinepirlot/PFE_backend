import unittest
from unittest.mock import Mock

from app.main import app
from data.services.DALService import DALService


class ChatRoomsTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.dal_service = DALService()
        self.dal_service.start = Mock()
        self.dal_service.commit_transaction = Mock()
        self.dal_service.rollback_transaction = Mock()
        self.chatroom_from_db = [[(25, 1, 2)]]
        self.chatroom_json = {"id_room": 25, "id_user1": 1, "id_user2": 2}

    def test_get_chat_room_by_id(self):
        self.dal_service.execute = Mock(return_value=self.chatroom_from_db)
        response = self.app.get('/chat_rooms/getRoomById/25')
        self.assertEqual(201, response.status_code)
        self.assertEqual(self.chatroom_json, response.get_json())

    def test_get_chat_room_by_id_with_non_existent_id(self):
        self.dal_service.execute = Mock(return_value=[[]])
        response = self.app.get('/chat_rooms/getRoomById/2500')
        self.assertEqual(404, response.status_code)
