class Appointment:
    def __init__(self, id_course, id_student, appointment_state, appointment_date, street, number_house, box_house):
        self.id_course = id_course
        self.id_student = id_student
        self.appointment_state = appointment_state
        self.appointment_date = appointment_date
        self.street = street
        self.number_house = number_house
        self.box_house = box_house

    def get_appointment_state(self):
        return self.appointment_state

    def convert_to_json(self):
        return {
            "id_course": self.id_course,
            "id_student": self.id_student,
            "appointment_state": self.appointment_state,
            "appointment_date": self.appointment_date,
            "street": self.street,
            "number_house": self.number_house,
            "box_house": self.box_house,
        }