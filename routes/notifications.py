from flask import Blueprint, jsonify, request, abort

from Exceptions.WebExceptions.BadRequestException import BadRequestException
from services.NotificationsService import NotificationsService
from models.Notification import Notification
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
    return notifications


@route.route('', methods=['POST'])
def add_notification():
    json = prevent_xss(request.json)
    print(json['chat_link'])
    if json['chat_link'] is None:
        notification = Notification(int(json['id_user']), str(json['notification_text']), None)
    else:
        notification = Notification(int(json['id_user']), str(json['notification_text']), str(json['chat_link']))

    notification_service.add_notification(notification)
    return jsonify({'notification': 'notification created'})


@route.route('/update/<int:id_notification>', methods=['PUT'])
def update_notification(id_notification):
    print(id_notification)
    notification_service.update_notification(id_notification)
    return jsonify({"update done": "notification"})


@route.route('/newNotif/<int:id_user>', methods=['GET'])
def isNewNotification(id_user):
    result = notification_service.isNewNotification(id_user)
    notifications = []
    for notification in result:
        notifications.append(notification.convert_to_json())
    return notifications
