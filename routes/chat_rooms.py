from flask import Blueprint, abort

from services.ChatRoomsService import ChatRoomsService

chat_rooms_service = ChatRoomsService()

route = Blueprint("chat_rooms", __name__)


# #########
# ###GET###
# #########
@route.route('/<int:id_user1>/<int:id_user2>', methods=['GET'])
def get_chat_room(id_user1, id_user2):
    chat_room = chat_rooms_service.get_chat_room(id_user1, id_user2)
    return chat_room.convert_to_json()


@route.route('/getRoomById/<id_room>', methods=['GET'])
def get_chat_room_by_id(id_room):
    chat_room = chat_rooms_service.get_chat_room_by_id(id_room)
    return chat_room.convert_to_json()


# ########
# ##POST##
# ########
@route.route("/<int:id_user1>/<int:id_user2>", methods=["POST"])
def create_chat_room(id_user1, id_user2):
    if id_user1 == id_user2:
        abort(412, "You cannot have a chat room with yourself.")
    return chat_rooms_service.create_chat_room(id_user1, id_user2).convert_to_json(), 201

# #########
# ###PUT###
# #########

# ############
# ###DELETE###
# ############
