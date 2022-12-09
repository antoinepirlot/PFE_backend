from flask import Blueprint, jsonify, request
from requests import HTTPError

from services.UsersService import UsersService

users_service = UsersService()

route = Blueprint("authentications", __name__)