from data.NotificationsDAO import NotificationsDAO


class NotificationsService:
    NotificationsDAO = NotificationsDAO()

    def __init__(self):
        pass

    def get_notification_from_user(self, id_user):
        return self.NotificationsDAO.get_notification_from_user(id_user)

    def add_notification(self, notification):
        return self.NotificationsDAO.add_notification(notification)
