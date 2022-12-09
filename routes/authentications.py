import jwt
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from requests import HTTPError
import os

from services.UsersService import UsersService

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
        return "Login object is not in the good format", 400

    user = users_service.get_users_by_email(data['email'])

    payload_data = {
        "id": user.convert_to_json()['id_user'],
        'exp': datetime.utcnow() + timedelta(minutes=10) #expiration time
    }

    my_secret = os.getenv("JWT_SECRET")

    token = jwt.encode(
        payload=payload_data,
        key=my_secret,
    )

    return token, 200