from flask import Blueprint, jsonify, request, abort

from services.NotificationsService import NotificationsService
from models.Notification import Notification

notification_service = NotificationsService()

route = Blueprint("notification", __name__)


# #########
# ###GET###
# #########
@route.route('/<int:id_user>', methods=['GET'])
def getNotificationFromUser(id_user):
    try:
        result = notification_service.getNotificationFromUser(id_user)
        users = []
        for user in result:
            users.append(user.convert_to_json())

        return users, 200
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500

@route.route('', methods=['POST'])
def add_notification():
    try:
        notification_service.add_notification(request.json)
        return jsonify({'notification': 'notification created'}), 201
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500