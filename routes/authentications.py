import os
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, jsonify, request

from Exceptions.WebExceptions.BadRequestException import BadRequestException
from services.UsersService import UsersService
from utils.security import prevent_xss

users_service = UsersService()

route = Blueprint("authentications", __name__)


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
    user = users_service.logInUser(data['email'], data['password'])
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


@route.route('/token/<string:token>', methods=['GET'])
def get_user_by_token(token):
    my_secret = os.getenv("JWT_SECRET")
    info_token = jwt.decode(token, key=my_secret, algorithms="HS256")

    result = users_service.get_users_by_token(info_token)

    return result.convert_to_json()
