from data.services.DALService import DALService
from models.Notification import Notification

import data.database as database
import models.User as User
import psycopg2


class NotificationsDAO:

    def __init__(self):
        self.dal = DALService()
        pass

    def get_notification_from_user(self, id_user):

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

    def add_notification(self, notification):
        connection = database.initialiseConnection()
        cursor = connection.cursor()
        sql = "INSERT INTO projet.notifications VALUES (DEFAULT,'%s','%s',now(),FALSE)" % (
            notification['id_user'], notification['notification_text'])
        try:

            cursor.execute(sql)
            connection.commit()

        except (Exception, psycopg2.DatabaseError) as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise Exception from e
            except IndexError:
                connection.rollback()
                print("SQL Error: %s" % str(e))
                raise Exception from e
        finally:
            cursor.close()
            connection.close()

