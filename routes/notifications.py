from flask import Blueprint, jsonify, request, abort

from services.NotificationsService import NotificationsService
from models.Notification import Notification

notification_service = NotificationsService()

route = Blueprint("notification", __name__)


# #########
# ###GET###
# #########
@route.route('/<int:id_user>', methods=['GET'])
def get_notification_from_user(id_user):
    result = notification_service.get_notification_from_user(id_user)
    users = []
    for user in result:
        users.append(user.convert_to_json())

    return users


@route.route('', methods=['POST'])
def add_notification():
    notification_service.add_notification(request.json)
    return jsonify({'notification': 'notification created'})
