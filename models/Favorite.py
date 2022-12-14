class Favorite:
    def __init__(self, id_teacher, id_student=None):
        self._id_teacher = id_teacher
        self._id_student = id_student

    @property
    def id_teacher(self):
        return self._id_teacher

    @property
    def id_student(self):
        return self._id_student

    @id_student.setter
    def id_student(self, id_student):
        self._id_student = id_student

    @classmethod
    def init_favorite_with_json(cls, json):
        return cls(json["id_teacher"])

    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        return {
            "id_teacher": self._id_teacher,
            "id_student": self._id_student,
        }
