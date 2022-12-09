from flask import Blueprint, jsonify, request, abort

from services.FavoritesService import FavoritesService
from models.Favorite import Favorite

favorites_service = FavoritesService()

route = Blueprint("favorites", __name__)


# #########
# ###GET###
# #########
@route.route('/<int:id_user>', methods=['GET'])
def get_favorites_from_user(id_user):
    try:
        result = favorites_service.get_favorites_from_user(id_user)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


# ########
# ##POST##
# ########
@route.route("/", methods=["POST"])
def add_favorite():
    try:
        favorites_service.add_favorite(request.json)
        return jsonify({'favorite': 'favorite added'}), 201
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500

# #########
# ###PUT###
# #########

# ############
# ###DELETE###
# ############
