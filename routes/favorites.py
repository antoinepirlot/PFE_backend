from flask import Blueprint, jsonify, request

from Exceptions.WebExceptions.BadRequestException import BadRequestException
from Exceptions.WebExceptions.ConflictException import ConflictException
from Exceptions.WebExceptions.NotFoundException import NotFoundException
from models.Favorite import Favorite
from services.FavoritesService import FavoritesService
from utils.authorize import authorize, get_id_from_token

favorites_service = FavoritesService()

route = Blueprint("favorites", __name__)


# #########
# ###GET###
# #########
@route.route('/<int:id_teacher>', methods=['GET'])
@authorize
def get_favorite(id_teacher):
    id_student = get_id_from_token(request.headers["authorization"])
    favorite = favorites_service.get_favorite(id_teacher, id_student)
    return favorite.convert_to_json()


@route.route('/<int:id_user>', methods=['GET'])
def get_favorites_from_user(id_user):
    all_favorites = favorites_service.get_favorites_from_user(id_user)
    all_favorites_json = []
    for favorite in all_favorites:
        all_favorites_json.append(favorite.convert_to_json())
    return all_favorites_json


@route.route('/mostFavoritesTeachers', methods=['GET'])
def get_most_favorites_teachers():
    all_favorites = favorites_service.get_most_favorites_teachers()
    return all_favorites


# ########
# ##POST##
# ########
@route.route("/", methods=["POST"])
@authorize
def add_favorite():
    new_favorite = Favorite.init_favorite_with_json(request.json)
    new_favorite.id_student = get_id_from_token(request.headers["authorization"])

    if new_favorite.id_teacher == new_favorite.id_student:
        raise BadRequestException("You cannot add yourself to your favorites")
    try:
        result = favorites_service.get_favorite(new_favorite.id_teacher, new_favorite.id_student)
    except NotFoundException:
        return favorites_service.add_favorite(new_favorite).convert_to_json(), 201
    raise ConflictException


# #########
# ###PUT###
# #########

# ############
# ###DELETE###
# ############
@route.route("/<int:id_teacher>", methods=["DELETE"])
@authorize
def remove_favorite(id_teacher):
    id_student = get_id_from_token(request.headers["authorization"])
    favorites_service.remove_favorite(id_teacher, id_student)
    return jsonify({'favorite': 'favorite deleted'}), 201
