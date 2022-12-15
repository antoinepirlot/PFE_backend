from flask import Blueprint, jsonify, request

from Exceptions.WebExceptions.BadRequestException import BadRequestException
from Exceptions.WebExceptions.ConflictException import ConflictException
from Exceptions.WebExceptions.ForbiddenException import ForbiddenException
from Exceptions.WebExceptions.NotFoundException import NotFoundException
from models.Favorite import Favorite
from services.FavoritesService import FavoritesService
from services.UsersService import UsersService
from utils.authorize import authorize, get_id_from_token

favorites_service = FavoritesService()
users_service = UsersService()

route = Blueprint("favorites", __name__)


# #########
# ###GET###
# #########
@route.route('/one/<int:id_teacher>', methods=['GET'])
@authorize
def get_favorite(id_teacher):
    id_student = get_id_from_token(request.headers["authorization"])
    if id_teacher is id_student:
        raise ForbiddenException(
            "It's your profile, you don't have a like for yourself"
        )
    favorite = favorites_service.get_favorite(id_teacher, id_student)
    return favorite.convert_to_json()


@route.route('/<int:id_user>', methods=['GET'])
def get_favorites_from_user(id_user):
    all_favorites = favorites_service.get_favorites_from_user(id_user)
    all_favorites_json = []
    for favorite in all_favorites:
        user = users_service.get_users_by_id(favorite.id_teacher)
        all_favorites_json.append({"teacher_username": user.pseudo})
    return all_favorites_json


# ########
# ##POST##
# ########
@route.route("/", methods=["POST"])
@authorize
def add_favorite():
    new_favorite = Favorite.init_favorite_with_json(request.json)
    new_favorite.id_student = get_id_from_token(request.headers["authorization"])
    if new_favorite.id_teacher is new_favorite.id_student:
        raise BadRequestException("You can't add yourself in your favorites")
    return favorites_service.add_favorite(new_favorite).convert_to_json(), 201

# ############
# ###DELETE###
# ############
@route.route("/<int:id_teacher>", methods=["DELETE"])
@authorize
def remove_favorite(id_teacher):
    id_student = get_id_from_token(request.headers["authorization"])
    favorites_service.remove_favorite(id_teacher, id_student)
    return jsonify({'favorite': 'favorite deleted'}), 201
