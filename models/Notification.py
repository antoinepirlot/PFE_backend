class Notification:
    def __init__(self, id_notification, id_user, notification_text, notification_date, seen):
        self.id_notification = id_notification
        self.id_user = id_user
        self.notification_text = notification_text
        self.notification_date = notification_date
        self.seen = seen

    def convert_to_json(self):
        return {"id_notification": self.id_notification,
                "id_user": self.id_user,
                "notification_text": self.notification_text,
                "notification_date": self.notification_date,
                "seen": self.seen
                }
