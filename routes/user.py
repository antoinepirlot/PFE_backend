from services.UsersService import UsersService

from flask import Flask, jsonify, request
from flask import Blueprint

route = Blueprint("user", __name__)
users_service = UsersService()


@route.route('/users', methods=['GET'])
def get_users():
    try:

        result = users_service.get_users()

        return jsonify(result), 200
    except (Exception) as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


@route.route('/users/<int:id_user>', methods=['GET'])
def get_user_by_id(id_user):
    try:
        result = users_service.get_users_by_id(id_user)
        return jsonify(result), 200
    except (Exception) as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


@route.route('/users', methods=['POST'])
def add_user():
    try:
        users_service.singInUser(request.json)
        return jsonify({'user': 'user created'}), 201
    except (Exception) as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500
