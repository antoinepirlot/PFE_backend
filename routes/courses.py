from flask import Blueprint, request, abort, Response, jsonify
from requests import HTTPError

from services.CoursesService import CoursesService
from models.Course import Course

courses_service = CoursesService()

route = Blueprint("courses", __name__)


# #########
# ###GET###
# #########
@route.route("/<id_course>", methods=["GET"])
def get_one(id_course):
    id_course = int(id_course)
    if id_course < 1:
        abort(400, "No id course lower than 1")
    course = courses_service.get_one(id_course)
    if course is None:
        abort(404, f"No course matching id: {id_course}")
    return 200, course



# ########
# ##POST##
# ########
@route.route("/", methods=["POST"])
def create_one():
    # check body is not empty
    if request.json['id_category'] is None or (not isinstance(request.json['id_category'], int)) or\
            request.json['id_category'] < 1 or request.json['id_teacher'] is None or \
            (not isinstance(request.json['id_teacher'], int)) or request.json['id_teacher'] < 1 or \
            request.json['course_description'] is None or len(str(request.json['course_description']).strip()) == 0 or \
            request.json['price_per_hour'] is None or (not isinstance(request.json['price_per_hour'], int)) or \
            request.json['price_per_hour'] <= 0 or request.json['city'] is None or \
            len(str(request.json['city']).strip()) == 0 or request.json['country'] is None or \
            len(str(request.json['country']).strip()) == 0 or request.json['id_level'] is None or \
            (not isinstance(request.json['id_level'], int)) or request.json['id_level'] < 1:
        return "Course is not in the good format", 400

    new_course = Course(request.json['id_category'], request.json['id_teacher'], request.json['course_description'],
                        request.json['price_per_hour'], request.json['city'], request.json['country'],
                        request.json['id_level'])
    return courses_service.create_one_course(new_course).convert_to_json(), 201
# #########
# ###PUT###
# #########


# ############
# ###DELETE###
# ############
