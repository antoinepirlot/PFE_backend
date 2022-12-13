import jwt
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound
import os

import utils.authorize
from Exceptions.WebExceptions.BadRequestException import BadRequestException
from services.UsersService import UsersService
from utils.authorize import get_id_from_token, authorize

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


@route.route('/', methods=['GET'])
@authorize
def get_user_by_token():
    id_user = get_id_from_token(request.headers["Authorization"])
    result = users_service.get_users_by_id(id_user)
    return result.convert_to_json()
