from flask import abort
from werkzeug.exceptions import NotFound

import data.database as database
import uuid
from models.ChatRoom import ChatRoom
import psycopg2


class ChatRoomsDAO:
    def __init__(self):
        pass

    def get_chat_room(self, id_user1, id_user2):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT id_room, id_user1, id_user2 FROM projet.chat_rooms " \
              "WHERE (id_user1 = %i AND id_user2 = %i) OR (id_user1 =%i AND id_user2 = %i)" % (
                  id_user1, id_user2, id_user2, id_user1
              )
        try:
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchone()
            if result is None:
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
        finally:
            cursor.close()
            connection.close()

    def get_chat_room_by_id(self, id_room):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "SELECT id_room, id_user1, id_user2 FROM projet.chat_rooms " \
              "WHERE id_room = '%s'" % (
                  id_room
              )
        try:
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchone()
            if result is None:
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
        finally:
            cursor.close()
            connection.close()

    def create_chat_room(self, id_user1, id_user2):
        id_room = str(uuid.uuid4())
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "INSERT INTO projet.chat_rooms(id_room, id_user1, id_user2)" \
              " VALUES('%s', %i, %i)" % (id_room, id_user1, id_user2)
        try:
            cursor.execute(sql)
            connection.commit()
            chat_room = ChatRoom(str(id_room), int(id_user1), int(id_user2))
            return chat_room
        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise Exception from e
        finally:
            cursor.close()
            connection.close()
