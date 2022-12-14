from data.DAO.AppointmentsDAO import AppointmentsDAO

from data.services.DALService import DALService


class AppointmentsService:

    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of AppointmentsService class, a new one is created
            cls._appointments_DAO = AppointmentsDAO()
            cls._dal = DALService()
            cls._instance = super(AppointmentsService, cls).__new__(cls)
        # There's already an instance of AppointmentsService class, so the existing one is returned
        return cls._instance

    def get_appointments_for_user(self, id_student):
        """
        Get all appointments of user, from the database.
        :param: id_student: the student's id
        :return: the list of appointments. If there's no appointments, it returns None
        """
        try:
            self._dal.start()
            users = self._appointments_DAO.get_appointments_for_user(id_student)
            self._dal.commit_transaction()
            return users
        except Exception as e:
            self._dal.rollback_transaction()
            raise e



    def get_appointment_for_user_of_course(self, id_course, id_student):
        """
        Get appointment of user and course, from the database.
        :param: id_course: the course id
        :param: id_student: the student's id
        :return: the appointment. If there's no appointment, it returns None
        """
        try:
            self._dal.start()
            appointment = self._appointments_DAO.get_appointment_for_user_of_course(id_course, id_student)
            self._dal.commit_transaction()
            return appointment
        except Exception as e:
            self._dal.rollback_transaction()
            raise e


    def update_appointments_state(self, id_course, id_student, appointment_state):
        """
        Update an appointment state, from the database.
        :param: id_course: the course id
        :param: id_student: the student's id
        :param: appointment_state: the state for the appointment
        """
        try:
            self._dal.start()
            self._appointments_DAO.update_appointment_state(id_course, id_student, appointment_state)
            self._dal.commit_transaction()
        except Exception as e:
            self._dal.rollback_transaction()
            raise e

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
        try:
            self._dal.start()
            result = self._appointments_DAO.create_appointement(id_course, id_student, appointment_date, street,
                                                               number_house, box_house)
            self._dal.commit_transaction()
            return result
        except Exception as e:
            self._dal.rollback_transaction()
            raise e

    def create_appointements_without_box_house(self, id_course, id_student, appointment_date, street, number_house):
        """
        Create a new appointment without the parameter box_house.
        :param: id_course: the course id
        :param: id_student: the student's id
        :param: appointment_date: the date for the appointment
        :param: street: the street for the appointment
        :param: number_house: number_house for the appointment
        """
        try:
            self._dal.start()
            result = self._appointments_DAO.create_appointement_without_box_house(id_course, id_student, appointment_date,
                                                                                 street,
                                                                                 number_house)
            self._dal.commit_transaction()
            return result
        except Exception as e:
            self._dal.rollback_transaction()
            raise e
