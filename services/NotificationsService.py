from data.NotificationsDAO import NotificationsDAO
from data.services.DALService import DALService


class NotificationsService:
    _notifications_dao = NotificationsDAO()
    _dal_service = DALService()

    def __init__(self):
        pass

    def get_notification_from_user(self, id_user):
        try:
            self._dal_service.start()
            result = self._notifications_dao.get_notification_from_user(id_user)
            self._dal_service.commit_transaction()
            return result
        except Exception as e:
            self._dal_service.rollback_transaction()

    def add_notification(self, notification):
        try:
            self._dal_service.start()
            result = self._notifications_dao.add_notification(notification)
            self._dal_service.commit_transaction()
            return result
        except Exception as e:
            self._dal_service.rollback_transaction()
