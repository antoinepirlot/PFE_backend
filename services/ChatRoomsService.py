from flask import abort

from data.ChatRoomsDAO import ChatRoomsDAO
from data.services.DALService import DALService


class ChatRoomsService:
    def __init__(self):
        self._chat_rooms_DAO = ChatRoomsDAO()
        self._dal_service = DALService()

    def get_chat_room(self, id_user1, id_user2):
        try:
            self._dal_service.start()
            results = self._chat_rooms_DAO.get_chat_room(id_user1, id_user2)
            print(results.convert_to_json())
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
            results = self._chat_rooms_DAO.create_chat_room(id_user1,
                                                            id_user2)  # if it returns error, it means it already exists
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()

        # # TODO that's Antoine's solution :p
        # try:
        #     self._dal_service.start()
        #     results = self._chat_rooms_DAO.create_chat_room(id_user1, id_user2)  # if it returns error, it means it already exists
        #     self._dal_service.commit_transaction()
        #     return results
        # except Exception as e:
        #     self._dal_service.rollback_transaction()
