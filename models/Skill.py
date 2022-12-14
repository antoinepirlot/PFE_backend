class Skill:
    def __init__(self, id_category, id_teacher):
        self.id_category = id_category
        self.id_teacher = id_teacher
    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        return {
            "id_category": self.id_category,
            "id_teacher": self.id_teacher,
        }
