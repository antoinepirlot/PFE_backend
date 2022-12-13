import os
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, jsonify, request

import utils.authorize
from Exceptions.WebExceptions.BadRequestException import BadRequestException
from services.UsersService import UsersService
from utils.authorize import authorize
from utils.security import prevent_xss

users_service = UsersService()

route = Blueprint("authentications", __name__)


# #######
# ##GET##
# #######
@route.route('/token/', methods=['GET'])
@authorize
def get_user_by_token():
    id_user = utils.authorize.get_id_from_token(request.headers["authorize"])
    result = users_service.get_users_by_id(id_user)
    return result.convert_to_json()


# ########
# ##POST##
# ########
@route.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # check body
    if 'email' not in data or len(str(data['email']).strip()) == 0 or \
        'password' not in data or len(str(data['password']).strip()) == 0:
        raise BadRequestException("Login object is not in the good format")
    data = prevent_xss(data)
    user = users_service.login_user(data['email'], data['password'])
    payload_data = {
        "id": user['id_user'],
        'exp': datetime.utcnow() + timedelta(days=5)  # expiration time
    }

    my_secret = os.getenv("JWT_SECRET")

    token = jwt.encode(
        payload=payload_data,
        key=my_secret, algorithm="HS256"
    )

    return jsonify(token)
