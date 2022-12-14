from flask import Blueprint, jsonify, request, abort

from services.NotificationsService import NotificationsService
from models.Notification import Notification

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
    print(request.json['chat_link'])
    if request.json['chat_link'] is None:
        notification = Notification(int(request.json['id_user']), str(request.json['notification_text']))
    else:
        notification = Notification(int(request.json['id_user']), str(request.json['notification_text']), None, None,
                                    None, str(request.json['chat_link']))

    notification_service.add_notification(notification)
    return jsonify({'notification': 'notification created'}), 201
