import uuid

import psycopg2
from flask import abort
from werkzeug.exceptions import NotFound

from data.services.DALService import DALService
from models.ChatRoom import ChatRoom


class ChatRoomsDAO:
    def __init__(self):
        self._dal_service = DALService()

    def get_chat_room(self, id_user1, id_user2):
        sql = """
                    SELECT id_room, id_user1, id_user2 FROM projet.chat_rooms 
                    WHERE (id_user1 = %(id_user1)s AND id_user2 = %(id_user2)s) 
                       OR (id_user1 =%(id_user2)s AND id_user2 = %(id_user1)s);
                """
        values = {"id_user1": id_user1, "id_user2": id_user2}
        try:
            result = self._dal_service.execute(sql, values, True)[0]
            if result is None:
                # TODO move abort to route layer
                abort(404, "Chat room not found")

            chat_room = ChatRoom(result[0], result[1], result[2])

            print(chat_room)
            return chat_room
        except NotFound as not_found_e:
            raise not_found_e
        except (Exception, psycopg2.DatabaseError) as e:
            print("----------")
            print(type(e))
            print("----------")
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e

    def get_chat_room_by_id(self, id_room):
        sql = """
            SELECT id_room, id_user1, id_user2 FROM projet.chat_rooms 
            WHERE id_room = %(id_room)s;
        """
        values = {"id_room": id_room}
        try:
            result = self._dal_service.execute(sql, values, True)[0]
            if result is None:
                # TODO move abort to route layer
                abort(404, "Chat room not found")
            chat_room = ChatRoom(str(result[0]), int(result[1]), int(result[2]))
            return chat_room
        except NotFound as not_found_e:
            raise not_found_e
        except (Exception, psycopg2.DatabaseError) as e:
            print("----------")
            print(type(e))
            print("----------")
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e

    def create_chat_room(self, id_user1, id_user2):
        id_room = str(uuid.uuid4())
        sql = """
            INSERT INTO projet.chat_rooms(id_room, id_user1, id_user2)
            VALUES(%(id_room)s, %(id_user1)s, %(id_user2)s)
            RETURNING id_room, id_user1, id_user2
        """
        values = {"id_room": id_room, "id_user1": id_user1, "id_user2": id_user2}
        try:
            result = self._dal_service.execute(sql, values, True)
            print("voici le result : ", result)
            # TODO result is now a chat room, use these values from returned sql
            chat_room = ChatRoom(str(id_room), int(id_user1),
                                 int(id_user2))
            return chat_room
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e
