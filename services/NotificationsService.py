from data.DAO.NotificationsDAO import NotificationsDAO
from data.services.DALService import DALService


class NotificationsService:
    _notifications_dao = NotificationsDAO()
    _dal_service = DALService()

    def __init__(self):
        pass

    def get_notifications_from_user(self, id_user):
        """
        Get all notifications of a user
        :param id_user: the id of the user
        :return: all notifications for the user specified
        """
        try:
            self._dal_service.start()
            result = self._notifications_dao.get_notifications_from_user(id_user)
            self._dal_service.commit_transaction()
            return result
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e

    def add_notification(self, notification):
        """
        Add a notification for a user
        :param notification: object notification with id_user and notification text
        """
        try:
            self._dal_service.start()
            self._notifications_dao.add_notification(notification)
            self._dal_service.commit_transaction()
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e
