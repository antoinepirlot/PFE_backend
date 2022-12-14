import uuid

import psycopg2
from flask import abort
from werkzeug.exceptions import NotFound

from data.services.DALService import DALService
from models.ChatRoom import ChatRoom


class ChatRoomsDAO:
    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of ChatRoomsDAO class, a new one is created
            cls._dal = DALService()
            cls._instance = super(ChatRoomsDAO, cls).__new__(cls)
        # There's already an instance of ChatRoomsDAO class, so the existing one is returned
        return cls._instance

    def get_chat_room(self, id_user1, id_user2):
        """
        Get the chat room of 2 users
        :param id_user1: id of the first user
        :param id_user2: id of the second user
        :return: a chat room
        """
        sql = """
            SELECT id_room, id_user1, id_user2 FROM projet.chat_rooms 
            WHERE (id_user1 = %(id_user1)s AND id_user2 = %(id_user2)s) 
               OR (id_user1 =%(id_user2)s AND id_user2 = %(id_user1)s);
        """
        values = {"id_user1": id_user1, "id_user2": id_user2}
        result = self._dal.execute(sql, values, True)[0]
        if result is None:
            return None
        chat_room = ChatRoom(result[0], result[1], result[2])
        return chat_room

    def get_chat_room_by_id(self, id_room):
        """
        Get a chat room by its id
        :param id_room: the id of the chat room
        :return: the chat room with the good id
        """
        sql = """
            SELECT id_room, id_user1, id_user2 FROM projet.chat_rooms 
            WHERE id_room = %(id_room)s;
        """
        values = {"id_room": id_room}
        result = self._dal.execute(sql, values, True)[0]
        if result is None:
            return None
        chat_room = ChatRoom(result[0], result[1], result[2])
        return chat_room

    def create_chat_room(self, id_user1, id_user2):
        """
        Create one chat room
        :param id_user1: id of the first user
        :param id_user2: id of the second user
        :return: the created chat room
        """
        id_room = str(uuid.uuid4())
        sql = """
            INSERT INTO projet.chat_rooms(id_room, id_user1, id_user2)
            VALUES(%(id_room)s, %(id_user1)s, %(id_user2)s)
            RETURNING id_room, id_user1, id_user2
        """
        values = {"id_room": id_room, "id_user1": id_user1, "id_user2": id_user2}
        self._dal.execute(sql, values, True)

        chat_room = ChatRoom(id_room, id_user1, id_user2)
        return chat_room
