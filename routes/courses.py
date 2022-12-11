from flask import Blueprint, request, abort, jsonify

from models.Course import Course
from services.CoursesService import CoursesService

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
    return course, 200


@route.route("/teacher/<id_teacher>", methods=["GET"])
def get_all_courses_from_teacher(id_teacher):
    id_teacher = int(id_teacher)
    if id_teacher < 1:
        abort(400, "No id teacher lower than 1")
    courses = courses_service.get_all_courses_from_teacher(id_teacher)
    if courses is None:
        abort(404, f"No courses for teacher's id {id_teacher}")
    return courses, 200


# ########
# ##POST##
# ########
@route.route("/", methods=["POST"])
def create_one():
    # check body is not empty
    if 'id_category' not in request.get_json() or (not isinstance(request.json['id_category'], int)) or \
            request.json['id_category'] < 1 or 'id_teacher' not in request.get_json() or \
            (not isinstance(request.json['id_teacher'], int)) or request.json['id_teacher'] < 1 or \
            'course_description' not in request.get_json() or len(
        str(request.json['course_description']).strip()) == 0 or \
            'price_per_hour' not in request.get_json() or (not isinstance(request.json['price_per_hour'], int) and
                                                           not isinstance(request.json['price_per_hour'], float)) or \
            request.json['price_per_hour'] <= 0 or 'city' not in request.get_json() or \
            len(str(request.json['city']).strip()) == 0 or 'country' not in request.get_json() or \
            len(str(request.json['country']).strip()) == 0 or 'level' not in request.get_json() or \
            len(str(request.json['level']).strip()) == 0 or str(request.json['level']) not in ["Débutant",
                                                                                               "Intermédiaire",
                                                                                               "Confirmé"]:
        return "Course is not in the good format", 400

    new_course = Course(request.json['id_category'], request.json['id_teacher'], request.json['course_description'],
                        request.json['price_per_hour'], request.json['city'], request.json['country'],
                        request.json['level'])
    try:
        return courses_service.create_one_course(new_course).convert_to_json(), 201
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500
# #########
# ###PUT###
# #########


# ############
# ###DELETE###
# ############
