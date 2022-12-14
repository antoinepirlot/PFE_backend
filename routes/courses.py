from flask import Blueprint, request

from Exceptions.WebExceptions.BadRequestException import BadRequestException
from models.Course import Course
from services.CoursesService import CoursesService
from utils.authorize import authorize, get_id_from_token
from utils.security import prevent_xss

courses_service = CoursesService()

route = Blueprint("courses", __name__)


# #########
# ###GET###
# #########

@route.route('', methods=['GET'])
def get_all_courses():
    filter_city = prevent_xss(request.args.get('city', default=None, type=str))
    filter_description = request.args.get('description', default=None, type=str)
    filter_name_course = prevent_xss(request.args.get('course', default=None, type=str))

    search_filters = []
    if filter_city and filter_city.strip():
        search_filters.append({"city": filter_city})
    if filter_description and filter_description.strip():
        search_filters.append({"description": filter_description})
    if filter_name_course and filter_name_course.strip():
        search_filters.append({"course": filter_name_course})

    print(search_filters)
    if len(search_filters) == 0:
        search_filters = None
    result = courses_service.get_all_courses(search_filters)
    courses = []
    for course in result:
        courses.append(course.convert_to_json())
    return courses, 200


@route.route("/<id_course>", methods=["GET"])
def get_one(id_course):
    id_course = int(id_course)
    if id_course < 1:
        raise BadRequestException("No id course lower than 1")
    course = courses_service.get_one(id_course)
    return course, 200


@route.route("/teacher", methods=["GET"])
@authorize
def get_all_courses_from_teacher():
    id_teacher = get_id_from_token(request.headers["Authorization"])
    print(id_teacher)
    if id_teacher < 1:
        raise BadRequestException("No id teacher lower than 1")
    result = courses_service.get_all_courses_from_teacher(id_teacher)
    courses = []
    for course in result:
        courses.append(course.convert_to_json())
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
            len(request.json['city'].strip()) == 0 or 'country' not in request.get_json() or \
            len(request.json['country'].strip()) == 0 or 'level' not in request.get_json() or \
            len(request.json['level'].strip()) == 0 or request.json['level'] not in ["Débutant",
                                                                                     "Intermédiaire",
                                                                                     "Confirmé"]:
        return BadRequestException("Course is not in the good format")
    json = prevent_xss(request.json)
    new_course = Course(json['id_category'], json['id_teacher'], json['course_description'],
                        json['price_per_hour'], json['city'], json['country'],
                        json['level'])
    return courses_service.create_one_course(new_course).convert_to_json(), 201
