from flask import abort
from werkzeug.exceptions import NotFound

from Exceptions.WebExceptions.NotFoundException import NotFoundException
from Exceptions.WebExceptions.ConflictException import ConflictException
from data.DAO.ChatRoomsDAO import ChatRoomsDAO
from data.services.DALService import DALService


class ChatRoomsService:
    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of ChatRoomsService class, a new one is created
            cls._dal = DALService()
            cls._chat_rooms_DAO = ChatRoomsDAO()
            cls._instance = super(ChatRoomsService, cls).__new__(cls)
        # There's already an instance of CategoriesService class, so the existing one is returned
        return cls._instance

    def get_chat_room(self, id_user1, id_user2):
        """
        Get the chat room of 2 users
        :param id_user1: id of the first user
        :param id_user2: id of the second user
        :return: a chat room
        """
        try:
            self._dal.start()
            results = self._chat_rooms_DAO.get_chat_room(id_user1, id_user2)
            if results is None:
                raise NotFoundException
            self._dal.commit_transaction()
            return results
        except Exception as e:
            self._dal.rollback_transaction()
            raise e

    def get_chat_room_by_id(self, id_room):
        """
        Get a chat room by its id
        :param id_room: the id of the chat room
        :return: the chat room with the good id
        """
        try:
            self._dal.start()
            results = self._chat_rooms_DAO.get_chat_room_by_id(id_room)
            if results is None:
                raise NotFoundException()
            self._dal.commit_transaction()
            return results
        except Exception as e:
            self._dal.rollback_transaction()
            raise e

    def create_chat_room(self, id_user1, id_user2):
        """
        Create one chat room
        :param id_user1: id of the first user
        :param id_user2: id of the second user
        :return: the created chat room
        """
        try:
            self._dal.start()
            # results = self._chat_rooms_DAO.create_chat_room(id_user1,id_user2)  # if it returns error, it means it
            # already exists
            """ dont want to work
            if self._chat_rooms_DAO.get_chat_room(id_user1, id_user2) is not None:
                self._dal_service.rollback_transaction()
                abort(409, "You already have a chat room with this user.")
            """
            results = self._chat_rooms_DAO.get_chat_room(id_user1, id_user2)
            if results is None:
                results = self._chat_rooms_DAO.create_chat_room(id_user1, id_user2)

            self._dal.commit_transaction()
            return results
        except Exception as e:
            self._dal.rollback_transaction()
            raise e

        # # TODO that's Antoine's solution :p
        # try:
        #     self._dal_service.start()
        #     results = self._chat_rooms_DAO.create_chat_room(id_user1, id_user2)  # if it returns error, it means it already exists
        #     self._dal_service.commit_transaction()
        #     return results
        # except Exception as e:
        #     self._dal_service.rollback_transaction()
