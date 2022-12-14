import psycopg2

from data.services.DALService import DALService
from models.Appointment import Appointment


class AppointmentsDAO:
    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of AppointmentsDAO class, a new one is created
            cls._dal = DALService()
            cls._instance = super(AppointmentsDAO, cls).__new__(cls)
        # There's already an instance of AppointmentsDAO class, so the existing one is returned
        return cls._instance

    def get_appointments_from_teacher_and_student(self, id_teacher, id_student):
        """
        Get all appointments of teacher and user, from the database.
        :param: id_teacher:  the teacher's id
        :param: id_student: the student's id
        :return: the list of appointments. If there's no appointments, it returns None
        """
        sql = "SELECT DISTINCT a.id_course, a.id_student, a.appointment_state, a.appointment_date, a.street, a.number_house, a.box_house " \
              "FROM projet.appointments a, projet.courses c " \
              "WHERE a.id_course = c.id_course AND a.id_student = %(id_student)s AND c.id_teacher = %(id_teacher)s"

        results = self._dal.execute(sql, {"id_teacher": id_teacher, "id_student": id_student}, True)
        if len(results) == 0:
            return None
        all_appointments = []
        for row in results:
            appointment = Appointment(int(row[0]), int(row[1]), str(row[2]), str(row[3]), str(row[4]), int(row[5]),
                                      str(row[6]))
            all_appointments.append(appointment)
        return all_appointments

    def get_appointments_for_user(self, id_student):
        """
        Get all appointments of user, from the database.
        :param: id_student: the student's id
        :return: the list of appointments. If there's no appointments, it returns None
        """
        sql = "SELECT DISTINCT id_course, id_student, appointment_state, appointment_date, street, number_house, box_house " \
              "FROM projet.appointments " \
              "WHERE  id_student = %(id_student)s ORDER BY appointment_state DESC, appointment_date"

        results = self._dal.execute(sql, {"id_student": id_student}, True)
        if len(results) == 0:
            return None
        all_appointments = []
        for row in results:
            appointment = Appointment(int(row[0]), int(row[1]), str(row[2]), str(row[3]), str(row[4]), int(row[5]),
                                      str(row[6]))
            all_appointments.append(appointment)
        return all_appointments

    def get_appointment_for_user_of_course(self, id_course, id_student):
        """
        Get appointment of user and course, from the database.
        :param: id_course: the course id
        :param: id_student: the student's id
        :return: the appointment. If there's no appointment, it returns None
        """
        sql = "SELECT DISTINCT id_course, id_student, appointment_state, appointment_date, street, number_house, box_house " \
              "FROM projet.appointments " \
              "WHERE  id_course = %(id_course)s AND id_student = %(id_student)s"

        result = self._dal.execute(sql, {"id_course": id_course, "id_student": id_student}, True)
        if len(result) == 0:
            return None
        result = result[0]
        appointment = Appointment(int(result[0]), int(result[1]), str(result[2]), str(result[3]), str(result[4]),
                                  int(result[5]), str(result[6]))
        return appointment

    def update_appointment_state(self, id_course, id_student, appointment_state):
        """
        Update an appointment state, from the database.
        :param: id_course: the course id
        :param: id_student: the student's id
        :param: appointment_state: the state for the appointment
        """
        sql = "UPDATE projet.appointments SET appointment_state = %(appointment_state)s " \
              "WHERE  id_course = %(id_course)s AND id_student = %(id_student)s"

        self._dal.execute(sql, {"id_course": int(id_course), "id_student": int(id_student),
                               "appointment_state": str(appointment_state)})

    def create_appointement(self, id_course, id_student, appointment_date, street, number_house, box_house):
        """
        Create a new appointment.
        :param: id_course: the course id
        :param: id_student: the student's id
        :param: appointment_date: the date for the appointment
        :param: street: the street for the appointment
        :param: number_house: number_house for the appointment
        :param: box_house: box_house for the appointment
        """
        sql = """
              INSERT INTO projet.appointments (id_course, id_student, appointment_state, appointment_date, 
              street, number_house, box_house) VALUES ( %(id_course)s, %(id_student)s, DEFAULT, %(appointment_date)s,
              %(street)s, %(number_house)s, %(box_house)s )
              """
        dico_variables = {
            "id_course": id_course,
            "id_student": id_student,
            "appointment_date": appointment_date,
            "street": street,
            "number_house": number_house,
            "box_house": box_house,
        }
        self._dal.execute(sql, dico_variables, False)
        appointment = Appointment(int(id_course), int(id_student), 'pending', str(appointment_date), str(street),
                                  int(number_house), str(box_house))
        return appointment

    def create_appointement_without_box_house(self, id_course, id_student, appointment_date, street, number_house):
        """
        Create a new appointment without the parameter box_house.
        :param: id_course: the course id
        :param: id_student: the student's id
        :param: appointment_date: the date for the appointment
        :param: street: the street for the appointment
        :param: number_house: number_house for the appointment
        """
        sql = """
              INSERT INTO projet.appointments (id_course, id_student, appointment_state, appointment_date, 
              street, number_house, box_house) VALUES ( %(id_course)s, %(id_student)s, DEFAULT, %(appointment_date)s,
              %(street)s, %(number_house)s, DEFAULT)
              """
        dico_variables = {
            "id_course": id_course,
            "id_student": id_student,
            "appointment_date": appointment_date,
            "street": street,
            "number_house": number_house
        }
        self._dal.execute(sql, dico_variables, False)
        appointment = Appointment(int(id_course), int(id_student), 'pending', str(appointment_date), str(street),
                                  int(number_house), None)
        return appointment
