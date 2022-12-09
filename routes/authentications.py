import jwt
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound
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

    try:
        user = users_service.logInUser(data['email'], data['password'])
        payload_data = {
            "id": user['id_user'],
            'exp': datetime.utcnow() + timedelta(minutes=10)  # expiration time
        }

        my_secret = os.getenv("JWT_SECRET")

        token = jwt.encode(
            payload=payload_data,
            key=my_secret,
        )

        return jsonify(token), 200
    except NotFound as not_found_e:
        return "Email or password incorrect", 404
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500

