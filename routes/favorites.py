from flask import Blueprint, jsonify, request, abort

from services.FavoritesService import FavoritesService
from models.Favorite import Favorite

favorites_service = FavoritesService()

route = Blueprint("favorites", __name__)


# #########
# ###GET###
# #########
@route.route('/<int:id_teacher>/<int:id_student>', methods=['GET'])
def get_favorite(id_teacher, id_student):
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
def add_favorite():
    new_favorite = Favorite.init_favorite_with_json(request.json)
    return favorites_service.add_favorite(new_favorite).convert_to_json(), 201


# #########
# ###PUT###
# #########

# ############
# ###DELETE###
# ############
@route.route("/", methods=["DELETE"])
def remove_favorite():
    try:
        print(request.json)
        favorites_service.remove_favorite(request.json)
        return jsonify({'favorite': 'favorite deleted'}), 201
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500
