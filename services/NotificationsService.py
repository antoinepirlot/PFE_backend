from data.DAO.NotificationsDAO import NotificationsDAO
from data.services.DALService import DALService


class NotificationsService:

    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of NotificationsService class, a new one is created
            cls._dal_service = DALService()
            cls._notifications_dao = NotificationsDAO()
            cls._instance = super(NotificationsService, cls).__new__(cls)
        # There's already an instance of NotificationsService class, so the existing one is returned
        return cls._instance

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

    def update_notification(self, id_notification):
        """
        Update an appointment state, from the database.
        :param: id_course: the course id
        :param: id_student: the student's id
        :param: appointment_state: the state for the appointment
        """
        try:
            self._dal_service.start()
            self._notifications_dao.update_notification(id_notification)
            self._dal_service.commit_transaction()
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e
