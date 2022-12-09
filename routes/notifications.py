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
        return jsonify(result), 200
    except Exception as e:
        return jsonify({e.__class__.__name__: e.args[0]}), 500