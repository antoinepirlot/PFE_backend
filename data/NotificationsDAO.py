from data.services.DALService import DALService
from models.Notification import Notification

import data.database as database
import models.User as User
import psycopg2


class NotificationsDAO:

    def __init__(self):
        self.dal = DALService()
        pass

    def getNotificationFromUser(self, id_user):

        sql = """SELECT *
        FROM projet.notifications 
        WHERE id_user = %(id_user)s ORDER BY notification_date DESC;"""

        resultsExportNotif = []
        value = {"id_user": id_user}
        self.dal.start()
        results = self.dal.commit(sql, value)

        for row in results:
            print(type(row[2]))
            notif = Notification(int(row[0]), int(row[1]), str(row[2]), str(row[3]), bool(row[4]))

            resultsExportNotif.append(notif)
        return resultsExportNotif

