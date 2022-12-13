import psycopg2

from data.services.DALService import DALService
from models.Notification import Notification


class NotificationsDAO:

    def __init__(self):
        self._dal_service = DALService()

    def get_notifications_from_user(self, id_user):
        """
        Get all notifications of a user
        :param id_user: the id of the user
        :return: all notifications for the user specified
        """
        sql = """
            SELECT *
            FROM projet.notifications 
            WHERE id_user = %(id_user)s ORDER BY notification_date DESC;
        """
        results_export_notif = []
        value = {"id_user": id_user}
        results = self._dal_service.execute(sql, value, True)
        for row in results:
            notif = Notification(int(row[1]), str(row[2]), int(row[0]), str(row[3]), bool(row[4]))
            results_export_notif.append(notif)
        return results_export_notif

    def add_notification(self, notification):
        sql = """
            INSERT INTO projet.notifications VALUES (DEFAULT,%(id_user)s,%(text)s,now(),FALSE) 
        """
        values = {"id_user": notification.id_user, "text": str(notification.notification_text)}
        self._dal_service.execute(sql, values)
