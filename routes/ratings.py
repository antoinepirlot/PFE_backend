from flask import Blueprint, request
from requests import HTTPError

from services.RatingsService import RatingsService
from models.Rating import Rating

ratings_service = RatingsService()

route = Blueprint("ratings", __name__)


#########
###GET###
#########
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


########
##POST##
########
@route.route("/", methods=["POST"])
def create_one():
    # check body is not empty
    if request.json['id_rater'] is None or (not isinstance(request.json['id_rater'], int)) or request.json['id_rater'] < 1 or \
            request.json['id_rated'] is None or (not isinstance(request.json['id_rated'], int)) or request.json['id_rated'] < 1 or \
            request.json['rating_text'] is None or len(str(request.json['rating_text']).strip()) == 0 or \
            request.json['rating_number'] is None or (not isinstance(request.json['rating_number'], int)) or \
            request.json['rating_number'] < 1 or request.json['rating_number'] > 5:
        return "Rating is not in the good format", 400
    new_rating = Rating.init_rating_with_json(request.json)
    return ratings_service.create_rating(new_rating)
