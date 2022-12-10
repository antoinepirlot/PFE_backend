from flask import abort
from werkzeug.exceptions import NotFound

from data.ChatRoomsDAO import ChatRoomsDAO


class ChatRoomsService:
    chat_rooms_DAO = ChatRoomsDAO()

    def __init__(self):
        pass

    def get_chat_room(self, id_user1, id_user2):
        return self.chat_rooms_DAO.get_chat_room(id_user1, id_user2)

    def get_chat_room_by_id(self, id_room):
        return self.chat_rooms_DAO.get_chat_room_by_id(id_room)

    def create_chat_room(self, id_user1, id_user2):
        if id_user1 == id_user2:
            abort(412, "You cannot have a chat room with yourself.")
        try:
            self.chat_rooms_DAO.get_chat_room(id_user1, id_user2)
            abort(409, "You already have a chat room with this user.")
        except NotFound as not_found_p:
            chat_room = self.chat_rooms_DAO.create_chat_room(id_user1, id_user2)

        return chat_room
