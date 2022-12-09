import jwt
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from requests import HTTPError

from services.UsersService import UsersService

users_service = UsersService()

route = Blueprint("authentications", __name__)

# ########
# ##POST##
# ########
@route.route("/login", methods=["POST"])
def login():
    # check body is not empty
    if request.json['email'] is None or len(str(request.json['email']).strip()) == 0 or \
            request.json['password'] is None or len(str(request.json['password']).strip()) == 0:
        return "Login object is not in the good format", 400

    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=10),  # Expiration time
        'email': request.json['email']
    }

    return jwt.encode(payload, "ok",algorithm='HS256'), 200

    #return courses_service.create_one_course(new_course).convert_to_json(), 201