class ChatRoom:
    def __init__(self, id_room, id_user1, id_user2):
        self._id_room = id_room
        self._id_user1 = id_user1
        self._id_user2 = id_user2

    @property
    def id_room(self):
        return self._id_room

    @property
    def id_user1(self):
        return self._id_user1

    @property
    def id_user2(self):
        return self._id_user2

    @classmethod
    def init_favorite_with_json(cls, json):
        return cls(json["id_room"], json["id_user1"], json["id_user2"])

    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        return {
            "id_room": self._id_room,
            "id_user1": self._id_user1,
            "id_user2": self._id_user2
        }
