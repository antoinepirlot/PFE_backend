class Notification:

    def __init__(self, id_user, notification_text, id_notification=None, notification_date=None, seen=None):
        self.id_notification = id_notification
        self._id_user = id_user
        self._notification_text = notification_text
        self.notification_date = notification_date
        self.seen = seen

    @property
    def id_user(self):
        return self._id_user

    @property
    def notification_text(self):
        return self._notification_text


    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        return {"id_notification": self.id_notification,
                "id_user": self.id_user,
                "notification_text": self.notification_text,
                "notification_date": self.notification_date,
                "seen": self.seen
                }
