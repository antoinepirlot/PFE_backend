from flask import Blueprint, request

from services.RatingsService import RatingsService

ratings_service = RatingsService()

route = Blueprint("ratings", __name__)


# #########
# ###GET###
# #########
@route.route('/', methods=['GET'])
def get_ratings_from_teacher():
    id_teacher = request.args.get('id_teacher')
    if id_teacher is None or int(id_teacher) < -1:
        return "ID of the teacher is not mentioned or negative", 400
    all_ratings = ratings_service.get_ratings(int(id_teacher))
    all_ratings_json = []
    for rating in all_ratings:
        all_ratings_json.append(rating.convert_to_json())
    return all_ratings_json

# ########
# ##POST##
# ########
