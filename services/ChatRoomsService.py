from flask import abort
from werkzeug.exceptions import NotFound

from data.ChatRoomsDAO import ChatRoomsDAO
from data.services.DALService import DALService


class ChatRoomsService:
    _chat_rooms_DAO = ChatRoomsDAO()
    _dal_service = DALService()

    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "instance"):
            # No instance of ChatRoomsService class, a new one is created
            cls.instance = super(ChatRoomsService, cls).__new__(cls)
        # There's already an instance of ChatRoomsService class, so the existing one is returned
        return cls.instance

    def get_chat_room(self, id_user1, id_user2):
        return self._chat_rooms_DAO.get_chat_room(id_user1, id_user2)

    def get_chat_room_by_id(self, id_room):
        return self._chat_rooms_DAO.get_chat_room_by_id(id_room)

    def create_chat_room(self, id_user1, id_user2):
        if id_user1 == id_user2:
            abort(412, "You cannot have a chat room with yourself.")
        try:
            self._chat_rooms_DAO.get_chat_room(id_user1, id_user2)
            abort(409, "You already have a chat room with this user.")
        except NotFound as not_found_p:
            chat_room = self._chat_rooms_DAO.create_chat_room(id_user1, id_user2)

        return chat_room
