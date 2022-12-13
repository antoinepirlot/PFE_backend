class Favorite:
    def __init__(self, id_teacher, id_student=None):
        self.id_teacher = id_teacher
        self.id_student = id_student

    @classmethod
    def init_favorite_with_json(cls, json):
        return cls(json["id_teacher"])

    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        return {
            "id_teacher": self.id_teacher,
            "id_student": self.id_student,
        }
