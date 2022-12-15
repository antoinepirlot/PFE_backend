import psycopg2
from sqlalchemy import true, false

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
            SELECT id_user, notification_text,chat_link, id_notification, notification_date, seen
            FROM projet.notifications 
            WHERE id_user = %(id_user)s ORDER BY notification_date DESC;
        """
        results_export_notif = []
        value = {"id_user": id_user}
        results = self._dal.execute(sql, value, True)
        for row in results:
            notif = Notification(int(row[0]), str(row[1]), str(row[2]), int(row[3]), str(row[4]), bool(row[5]))
            results_export_notif.append(notif)
        return results_export_notif

    def add_notification(self, notification):

        print("chat link", notification.chat_link)
        if notification.chat_link is None:
            sql = """
                        INSERT INTO projet.notifications VALUES (DEFAULT,%(id_user)s,%(text)s,now(),FALSE,DEFAULT) 
                    """
            values = {"id_user": notification.id_user, "text": str(notification.notification_text)}
            self._dal.execute(sql, values)
        else:
            sql = """
                            INSERT INTO projet.notifications VALUES (DEFAULT,%(id_user)s,%(text)s,now(),FALSE,%(chat_link)s) 
                        """

            values = {"id_user": notification.id_user, "text": str(notification.notification_text),
                      "chat_link": str(notification.chat_link)}
            self._dal.execute(sql, values)

    def update_notification(self, id_notification):
        """
        Update a notification of a user
        :param id_notification: notification to update
        """
        sql = """
            UPDATE projet.notifications SET seen = true WHERE id_notification = %(id_notification)s
                """

        print(id_notification)
        self._dal.execute(sql, {"id_notification": int(id_notification)})

    def isNewNotification(self, id_user):
        sql = """SELECT id_user, notification_text,chat_link, id_notification, notification_date, seen
            FROM projet.notifications 
            WHERE id_user = %(id_user)s AND seen = false;"""

        results_export_notif = []
        value = {"id_user": id_user}
        results = self._dal.execute(sql, value, True)
        for row in results:
            notif = Notification(int(row[0]), str(row[1]), str(row[2]), int(row[3]), str(row[4]), bool(row[5]))
            results_export_notif.append(notif)
        return results_export_notif
