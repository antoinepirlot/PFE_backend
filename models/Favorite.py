class Favorite:
    def __init__(self, id_teacher, id_student):
        self.id_teacher = id_teacher
        self.id_student = id_student

    def convert_to_json(self):
        return {"id_teacher": self.id_teacher,
                "id_student": self.id_student,
                }
