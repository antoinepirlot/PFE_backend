from flask import abort

from data.ChatRoomsDAO import ChatRoomsDAO
from data.services.DALService import DALService


class ChatRoomsService:
    def __init__(self):
        self._chat_rooms_DAO = ChatRoomsDAO()
        self._dal_service = DALService()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            # No instance of ChatRoomsService class, a new one is created
            cls.instance = super(ChatRoomsService, cls).__new__(cls)
        # There's already an instance of ChatRoomsService class, so the existing one is returned
        return cls.instance

    def get_chat_room(self, id_user1, id_user2):
        try:
            self._dal_service.start()
            results = self._chat_rooms_DAO.get_chat_room(id_user1, id_user2)
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()

    def get_chat_room_by_id(self, id_room):
        try:
            self._dal_service.start()
            results = self._chat_rooms_DAO.get_chat_room_by_id(id_room)
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()

    def create_chat_room(self, id_user1, id_user2):
        try:
            self._dal_service.start()
            # TODO use unique constraint in db and just use create chat room. If an error occur it means there's already a room
            self._chat_rooms_DAO.get_chat_room(id_user1, id_user2)
            abort(409, "You already have a chat room with this user.")
        except Exception as e:
            chat_room = self._chat_rooms_DAO.create_chat_room(id_user1, id_user2)
            return chat_room

        # # TODO that's Antoine's solution :p
        # try:
        #     self._dal_service.start()
        #     results = self._chat_rooms_DAO.create_chat_room(id_user1, id_user2)  # if it returns error, it means it already exists
        #     self._dal_service.commit_transaction()
        #     return results
        # except Exception as e:
        #     self._dal_service.rollback_transaction()
