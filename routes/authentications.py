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

    return 1

    #return courses_service.create_one_course(new_course).convert_to_json(), 201