class Skill:
    def __init__(self, id_category, id_teacher):
        self._id_category = id_category
        self._id_teacher = id_teacher

    @property
    def id_category(self):
        return self._id_category

    @property
    def id_teacher(self):
        return self._id_teacher

    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        return {
            "id_category": self._id_category,
            "id_teacher": self._id_teacher,
        }
