class Appointment:
    def __init__(self, id_course, id_student, appointment_state, appointment_date, street, number_house, box_house):
        self._id_course = id_course
        self._id_student = id_student
        self._appointment_state = appointment_state
        self._appointment_date = appointment_date
        self._street = street
        self._number_house = number_house
        self._box_house = box_house

    @property
    def id_course(self):
        return self._id_course

    @property
    def id_student(self):
        return self._id_student

    @property
    def appointment_state(self):
        return self._appointment_state

    @property
    def appointment_date(self):
        return self._appointment_date

    @property
    def street(self):
        return self._street

    @property
    def number_house(self):
        return self._number_house

    @property
    def box_house(self):
        return self._box_house

    def convert_to_json(self):
        """
        Convert the current object into json
        :return: a json that represents the current object
        """
        return {
            "id_course": self._id_course,
            "id_student": self._id_student,
            "appointment_state": self._appointment_state,
            "appointment_date": self._appointment_date,
            "street": self._street,
            "number_house": self._number_house,
            "box_house": self._box_house,
        }
