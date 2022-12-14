class Notification:

    def __init__(self, id_user, notification_text, id_notification=None, notification_date=None, seen=None):
        self._id_notification = id_notification
        self._id_user = id_user
        self._notification_text = notification_text
        self._notification_date = notification_date
        self._seen = seen

    @property
    def id_notification(self):
        return self._id_notification

    @property
    def id_user(self):
        return self._id_user

    @property
    def notification_text(self):
        return self._notification_text

    @property
    def notification_date(self):
        return self._notification_date

    @property
    def seen(self):
        return self._seen

    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        return {"id_notification": self._id_notification,
                "id_user": self._id_user,
                "notification_text": self._notification_text,
                "notification_date": self._notification_date,
                "seen": self._seen
                }
