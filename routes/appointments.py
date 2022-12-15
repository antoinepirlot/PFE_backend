from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound

from Exceptions.WebExceptions.BadRequestException import BadRequestException
from models.User import User
from services.AppointmentsService import AppointmentsService
from utils.security import prevent_xss
from utils.authorize import authorize

appointments_service = AppointmentsService()

route = Blueprint("appointments", __name__)


# #########
# ###GET###
# #########
@route.route('/<int:id_student>', methods=['GET'])
@authorize
def get_appointments(id_student):
    result = appointments_service.get_appointments_for_user(id_student)
    appointments = []
    for appointment in result:
        appointments.append(appointment.convert_to_json())
    return appointments


@route.route('/<int:id_course>/<int:id_student>', methods=['GET'])
def get_appointment_for_user_of_course(id_course, id_student):
    result = appointments_service.get_appointment_for_user_of_course(id_course, id_student)

    return result.convert_to_json()


@route.route('/<int:id_course>/<int:id_student>/state/<string:appointment_state>', methods=['PUT'])
def update_appointments_state(id_course, id_student, appointment_state):
    appointments_service.update_appointments_state(id_course, id_student, prevent_xss(appointment_state))
    return jsonify({"update done": ""})


# #########
# ###POST##
# #########
@route.route("/", methods=['POST'])
def create_one_appointement():
    # check body is not empty
    if 'id_course' not in request.get_json() or (not isinstance(request.json['id_course'], int)) or \
            request.json['id_course'] < 1 or 'id_student' not in request.get_json() or \
            (not isinstance(request.json['id_student'], int)) or request.json['id_student'] < 1 or \
            'appointment_date' not in request.get_json() or len(
        str(request.json['appointment_date']).strip()) == 0 or \
            'street' not in request.get_json() or len(
        str(request.json['street']).strip()) == 0 or \
            'number_house' not in request.get_json() or (not isinstance(request.json['number_house'], int) and
                                                         not isinstance(request.json['number_house'], float)) or \
            request.json['number_house'] <= 0:
        return BadRequestException("Appointement is not in the good format")
    json = prevent_xss(request.json)
    if 'box_house' not in json:
        return appointments_service.create_appointements_without_box_house(json['id_course'],
                                                                           json['id_student'],
                                                                           json['appointment_date'],
                                                                           json['street'], json[
                                                                               'number_house']).convert_to_json(), 201

    return appointments_service.create_appointements(json['id_course'], json['id_student'],
                                                     json['appointment_date'],
                                                     json['street'], json['number_house'],
                                                     json['box_house']).convert_to_json(), 201
