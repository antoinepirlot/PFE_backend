from flask import abort

from Exceptions.WebExceptions.NotFoundException import NotFoundException
from data.DAO.ChatRoomsDAO import ChatRoomsDAO
from data.services.DALService import DALService


class ChatRoomsService:
    def __init__(self):
        self._chat_rooms_DAO = ChatRoomsDAO()
        self._dal_service = DALService()

    def get_chat_room(self, id_user1, id_user2):
        """
        Get the chat room of 2 users
        :param id_user1: id of the first user
        :param id_user2: id of the second user
        :return: a chat room
        """
        try:
            self._dal_service.start()
            results = self._chat_rooms_DAO.get_chat_room(id_user1, id_user2)
            if results is None:
                raise NotFoundException()
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()

    def get_chat_room_by_id(self, id_room):
        """
        Get a chat room by its id
        :param id_room: the id of the chat room
        :return: the chat room with the good id
        """
        try:
            self._dal_service.start()
            results = self._chat_rooms_DAO.get_chat_room_by_id(id_room)
            if results is None:
                raise NotFoundException()
            self._dal_service.commit_transaction()
            return results
        except Exception as e:
            self._dal_service.rollback_transaction()

    def create_chat_room(self, id_user1, id_user2):
        """
        Create one chat room
        :param id_user1: id of the first user
        :param id_user2: id of the second user
        :return: the created chat room
        """
        try:
            self._dal_service.start()
            # results = self._chat_rooms_DAO.create_chat_room(id_user1,id_user2)  # if it returns error, it means it
            # already exists
            """ dont want to work
            if self._chat_rooms_DAO.get_chat_room(id_user1, id_user2) is not None:
                self._dal_service.rollback_transaction()
                abort(409, "You already have a chat room with this user.")
            """

            results = self._chat_rooms_DAO.create_chat_room(id_user1, id_user2)
            self._dal_service.commit_transaction()
            return results
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
