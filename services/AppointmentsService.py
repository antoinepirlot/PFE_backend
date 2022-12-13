from data.DAO.AppointmentsDAO import AppointmentsDAO

from data.services.DALService import DALService


class AppointmentsService:
    appointments_DAO = AppointmentsDAO()
    dal = DALService()

    def __init__(self):
        pass

    def get_appointments_for_user(self, id_student):
        self.dal.start()
        users = self.appointments_DAO.get_appointments_for_user(id_student)
        self.dal.commit_transaction()
        return users

    def get_appointments_for_user_of_course(self, id_course, id_student):
        self.dal.start()

        appointment = self.appointments_DAO.get_appointments_for_user_of_course(id_course, id_student)
        self.dal.commit_transaction()
        return appointment

    def update_appointments_state(self, id_course, id_student, appointment_state):
        self.dal.start()

        self.appointments_DAO.update_appointment_state(id_course, id_student, appointment_state)
        self.dal.commit_transaction()
