from data.DAO.AppointmentsDAO import AppointmentsDAO

from data.services.DALService import DALService


class AppointmentsService:
    appointments_DAO = AppointmentsDAO()
    dal = DALService()

    def __init__(self):
        pass

    def get_appointments_for_user(self, id_student):
        """
        Get all appointments of user, from the database.
        :param: id_student: the student's id
        :return: the list of appointments. If there's no appointments, it returns None
        """
        self.dal.start()
        users = self.appointments_DAO.get_appointments_for_user(id_student)
        self.dal.commit_transaction()
        return users

    def get_appointment_for_user_of_course(self, id_course, id_student):
        """
        Get appointment of user and course, from the database.
        :param: id_course: the course id
        :param: id_student: the student's id
        :return: the appointment. If there's no appointment, it returns None
        """
        self.dal.start()

        appointment = self.appointments_DAO.get_appointment_for_user_of_course(id_course, id_student)
        self.dal.commit_transaction()
        return appointment

    def update_appointments_state(self, id_course, id_student, appointment_state):
        """
        Update an appointment state, from the database.
        :param: id_course: the course id
        :param: id_student: the student's id
        :param: appointment_state: the state for the appointment
        """
        self.dal.start()

        self.appointments_DAO.update_appointment_state(id_course, id_student, appointment_state)
        self.dal.commit_transaction()

    def create_appointements(self, id_course, id_student, appointment_date, street, number_house, box_house):
        """
        Create a new appointment.
        :param: id_course: the course id
        :param: id_student: the student's id
        :param: appointment_date: the date for the appointment
        :param: street: the street for the appointment
        :param: number_house: number_house for the appointment
        :param: box_house: box_house for the appointment
        """
        self.dal.start()
        result = self.appointments_DAO.create_appointement(id_course, id_student, appointment_date, street,
                                                           number_house, box_house)
        self.dal.commit_transaction()
        return result

    def create_appointements_without_box_house(self, id_course, id_student, appointment_date, street, number_house):
        """
        Create a new appointment without the parameter box_house.
        :param: id_course: the course id
        :param: id_student: the student's id
        :param: appointment_date: the date for the appointment
        :param: street: the street for the appointment
        :param: number_house: number_house for the appointment
        """
        self.dal.start()
        result = self.appointments_DAO.create_appointement_without_box_house(id_course, id_student, appointment_date,
                                                                             street,
                                                                             number_house)
        self.dal.commit_transaction()
        return result
