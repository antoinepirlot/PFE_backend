from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound

from models.User import User
from services.AppointmentsService import AppointmentsService

appointments_service = AppointmentsService()

route = Blueprint("appointments", __name__)


# #########
# ###GET###
# #########
@route.route('/<int:id_student>', methods=['GET'])
def get_appointments(id_student):
    try:
        result = appointments_service.get_appointments_for_user(id_student)
        appointments = []
        for appointment in result:
            appointments.append(appointment.convert_to_json())
        return appointments, 200
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


@route.route('/<int:id_course>/<int:id_student>', methods=['GET'])
def get_appointments_for_user_of_course(id_course, id_student):
    try:
        result = appointments_service.get_appointments_for_user_of_course(id_course, id_student)

        return result.convert_to_json(), 200
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500


@route.route('/<int:id_course>/<int:id_student>/state/<string:appointment_state>', methods=['PUT'])
def update_appointments_state(id_course, id_student, appointment_state):
    try:
        appointments_service.update_appointments_state(id_course, id_student, appointment_state)

        return jsonify({"update done": ""}), 200
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500
