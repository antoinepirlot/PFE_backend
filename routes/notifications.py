from flask import Blueprint, jsonify, request

from Exceptions.WebExceptions.BadRequestException import BadRequestException
from models.Notification import Notification
from services.NotificationsService import NotificationsService
from utils.security import prevent_xss

notification_service = NotificationsService()

route = Blueprint("notification", __name__)


# #########
# ###GET###
# #########
@route.route('/<int:id_user>', methods=['GET'])
def get_notifications_from_user(id_user):
    result = notification_service.get_notifications_from_user(id_user)
    notifications = []
    for notification in result:
        notifications.append(notification.convert_to_json())
    return notifications, 200


@route.route('', methods=['POST'])
def add_notification():
    json = request.json
    if json is None \
            or (json["id_user"] is None or type(json["id_user"]) is not int) \
            and (json["notification_text"] is None or type(json["notification_text"]) is not str
                 or len(json["notification_text"]) == 0):
        raise BadRequestException("Wrong id_user in notification")
    notification = Notification(json['id_user'], prevent_xss(json['notification_text']))
    notification_service.add_notification(notification)
    return jsonify({'notification': 'notification created'}), 201
