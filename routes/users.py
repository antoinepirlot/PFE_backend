from flask import Blueprint, jsonify, request
from requests import HTTPError

from services.UsersService import UsersService

users_service = UsersService()

route = Blueprint("users", __name__)


# #########
# ###GET###
# #########
@route.route('', methods=['GET'])
def get_users():
    try:
        result = users_service.get_users()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


@route.route('/<int:id_user>', methods=['GET'])
def get_user_by_id(id_user):
    try:
        result = users_service.get_users_by_id(id_user)
        return result.convert_to_json(), 200
    except HTTPError as http_e:
        return http_e.args[1], http_e.args[0]
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


# ########
# ##POST##
# ########
@route.route('', methods=['POST'])
def add_user():
    try:
        users_service.singInUser(request.json)
        return jsonify({'user': 'user created'}), 201
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500

# #########
# ###PUT###
# #########

# ############
# ###DELETE###
# ############
