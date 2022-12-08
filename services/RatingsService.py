from flask import abort
from werkzeug.exceptions import NotFound

from data.RatingsDAO import RatingsDAO
from data.UsersDao import UsersDAO
from data.AppointmentsDAO import AppointmentsDAO


class RatingsService:
    ratings_DAO = RatingsDAO()
    users_DAO = UsersDAO()
    appointements_DAO = AppointmentsDAO()

    def __init__(self):
        pass

    def get_ratings(self, id_teacher):
        return self.ratings_DAO.get_ratings_from_teacher(id_teacher)

    def create_rating(self, rating):
        self.users_DAO.getUserById(rating.id_rater)
        self.users_DAO.getUserById(rating.id_rated)
        #check if a finish appointment exist
        appointment = self.appointements_DAO.get_appointments_from_teacher_and_student(rating.id_rated, rating.id_rater)
        if appointment[0].get_appointment_state() != 'finished':
            abort(403, "You have not finished the course with this teacher")
        #check if a rating already exist
        try:
            self.ratings_DAO.get_rating_by_id_rater_and_id_rated(rating.id_rater, rating.id_rated)
            abort(409, "You already give this teacher a rating.")
        except NotFound as not_found_e:
            #TODO create rating
            pass


        return rating

