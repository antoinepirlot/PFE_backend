import psycopg2

from data.services.DALService import DALService
from models.Notification import Notification


class NotificationsDAO:

    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of NotificationsDAO class, a new one is created
            cls._dal = DALService()
            cls._instance = super(NotificationsDAO, cls).__new__(cls)
        # There's already an instance of NotificationsDAO class, so the existing one is returned
        return cls._instance

    def get_notifications_from_user(self, id_user):
        """
        Get all notifications of a user
        :param id_user: the id of the user
        :return: all notifications for the user specified
        """
        sql = """
            SELECT id_user, notification_text, id_notification, notification_date, seen
            FROM projet.notifications 
            WHERE id_user = %(id_user)s ORDER BY notification_date DESC;
        """
        results_export_notif = []
        value = {"id_user": id_user}
        results = self._dal.execute(sql, value, True)
        for row in results:
            notif = Notification(int(row[0]), str(row[1]), int(row[2]), str(row[3]), bool(row[4]))
            results_export_notif.append(notif)
        return results_export_notif

    def add_notification(self, notification):

        print("chat link", notification.chat_link)
        if notification.chat_link is None:
            sql = """
                        INSERT INTO projet.notifications VALUES (DEFAULT,%(id_user)s,%(text)s,now(),FALSE,DEFAULT) 
                    """
            values = {"id_user": notification.id_user, "text": str(notification.notification_text)}
            self._dal_service.execute(sql, values)
        else:
            sql = """
                            INSERT INTO projet.notifications VALUES (DEFAULT,%(id_user)s,%(text)s,now(),FALSE,%(chat_link)s) 
                        """

            values = {"id_user": notification.id_user, "text": str(notification.notification_text), "chat_link": str(notification.chat_link)}
            self._dal_service.execute(sql, values)

