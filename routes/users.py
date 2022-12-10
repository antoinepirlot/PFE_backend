from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound

from models.User import User
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
        users = []
        for user in result:
            users.append(user.convert_to_json())

        return users, 200
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


@route.route('/<int:id_user>', methods=['GET'])
def get_user_by_id(id_user):
    try:
        result = users_service.get_users_by_id(id_user)
        return result.convert_to_json(), 200
    except NotFound as not_found_e:
        raise not_found_e
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


@route.route('/<string:email>', methods=['GET'])
def get_user_by_email(email):
    try:
        result = users_service.get_users_by_email(email)
        return result.convert_to_json(), 200
    except NotFound as not_found_e:
        raise not_found_e
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


@route.route('/pseudo/<string:pseudo>', methods=['GET'])
def get_user_by_pseudo(pseudo):
    try:

        result = users_service.get_users_by_pseudo(pseudo)
        return result.convert_to_json(), 200
    except NotFound as not_found_e:
        raise not_found_e
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


# ########
# ##POST##
# ########
@route.route('', methods=['POST'])
def add_user():
    try:
        users_service.sing_in_user(request.json)
        return jsonify({'user': 'user created'}), 201
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500

# #########
# ###PUT###
# #########

# ############
# ###DELETE###
# ############
