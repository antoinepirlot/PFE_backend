from data.DAO.AppointmentsDAO import AppointmentsDAO


from data.services.DALService import DALService


class AppointmentsService:
    appointments_DAO = AppointmentsDAO()
    dal = DALService()

    def __init__(self):
        pass

    def get_appointments_for_user(self, id_student):
        self.dal.start()
        try:
            users = self.appointments_DAO.get_appointments_for_user(id_student)
            self.dal.commit_transaction()
            return users
        except Exception as e:
            self.dal.rollback_transaction()
            raise e