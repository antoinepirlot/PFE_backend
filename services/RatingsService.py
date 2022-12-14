from Exceptions.WebExceptions.NotFoundException import NotFoundException
from Exceptions.WebExceptions.ConflictException import ConflictException
from Exceptions.WebExceptions.ForbiddenException import ForbiddenException
from data.DAO.AppointmentsDAO import AppointmentsDAO
from data.DAO.RatingsDAO import RatingsDAO
from data.DAO.UsersDAO import UsersDAO
from data.services.DALService import DALService


class RatingsService:

    def __init__(self):
        self.ratings_DAO = RatingsDAO()
        self.users_DAO = UsersDAO()
        self.appointements_DAO = AppointmentsDAO()
        self.dal = DALService()

    def get_ratings(self, id_teacher):
        """
        Get rating by the rated id (teacher).
        :param: id_teacher: the user's id that gets a rating
        :return: list of ratings, If there's no ratings, it returns None
        """
        self.dal.start()
        try:
            user = self.users_DAO.get_user_by_id(id_teacher)
            if user is None:
                raise NotFoundException("User not found")
            all_ratings = self.ratings_DAO.get_ratings_from_teacher(id_teacher)
            for rating in all_ratings:
                rater = self.users_DAO.get_user_by_id(rating.id_rater)
                rating.setRater(rater)
            self.dal.commit_transaction()
            return all_ratings
        except Exception as e:
            self.dal.rollback_transaction()
            raise e

    def create_rating(self, rating):
        """
        Create a rating in the database.
        :param: rating: the rating to add
        :return: the rating added.
        """
        self.dal.start()
        try:
            if self.users_DAO.get_user_by_id(rating.id_rater) is None:
                raise NotFoundException("The student rater doesn't exist")
            if self.users_DAO.get_user_by_id(rating.id_rated) is None:
                raise NotFoundException("The teacher rater doesn't exist")
            # check if a finish appointment exist
            appointments = self.appointements_DAO.get_appointments_from_teacher_and_student(rating.id_rated,
                                                                                            rating.id_rater)
            if appointments is None:
                raise ForbiddenException("You have no course with this teacher")
            isFinished = False
            for appointment in appointments:
                if appointment.appointment_state == 'finished':
                    isFinished = True
            if not isFinished:
                raise ForbiddenException("You have not finished the course with this teacher")
            # check if a rating already exist
            rating_db = self.ratings_DAO.get_rating_by_id_rater_and_id_rated(rating.id_rater, rating.id_rated)
            if rating_db is not None:
                raise ConflictException("You already give this teacher a rating")
            rating = self.ratings_DAO.create_one_rating(rating)
        except Exception as e:
            self.dal.rollback_transaction()
            raise e
        self.dal.commit_transaction()
        return rating
