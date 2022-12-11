from flask import abort

from data.RatingsDAO import RatingsDAO
from data.UsersDAO import UsersDAO
from data.AppointmentsDAO import AppointmentsDAO
from data.services.DALService import DALService


class RatingsService:

    def __init__(self):
        self.ratings_DAO = RatingsDAO()
        self.users_DAO = UsersDAO()
        self.appointements_DAO = AppointmentsDAO()
        self.dal = DALService()

    def get_ratings(self, id_teacher):
        self.dal.start()
        try:
            all_ratings = self.ratings_DAO.get_ratings_from_teacher(id_teacher)
            self.dal.commit_transaction()
            return all_ratings
        except Exception as e:
            self.dal.rollback_transaction()
            raise e

    def create_rating(self, rating):
        self.dal.start()
        try:
            if self.users_DAO.get_user_by_id(rating.id_rater) is None:
                abort(404, "The student rater doesn't exist")
            if self.users_DAO.get_user_by_id(rating.id_rated) is None:
                abort(404, "The teacher rated doesn't exist")
            # check if a finish appointment exist
            appointments = self.appointements_DAO.get_appointments_from_teacher_and_student(rating.id_rated, rating.id_rater)
            if appointments is None:
                abort(403, "You have no course with this teacher")
            isFinished = False
            for appointment in appointments:
                if appointment.get_appointment_state() == 'finished':
                    isFinished = True
            if not isFinished:
                abort(403, "You have not finished the course with this teacher")
            # check if a rating already exist
            rating_db = self.ratings_DAO.get_rating_by_id_rater_and_id_rated(rating.id_rater, rating.id_rated)
            if rating_db is not None:
                abort(409, "You already give this teacher a rating.")
            rating = self.ratings_DAO.create_one_rating(rating)
        except Exception as e:
            self.dal.rollback_transaction()
            raise e
        self.dal.commit_transaction()
        return rating
