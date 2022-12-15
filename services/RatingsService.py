from Exceptions.WebExceptions.NotFoundException import NotFoundException
from Exceptions.WebExceptions.ConflictException import ConflictException
from Exceptions.WebExceptions.ForbiddenException import ForbiddenException
from data.DAO.AppointmentsDAO import AppointmentsDAO
from data.DAO.NotificationsDAO import NotificationsDAO
from data.DAO.RatingsDAO import RatingsDAO
from data.DAO.UsersDAO import UsersDAO
from data.services.DALService import DALService
from models.Notification import Notification


class RatingsService:

    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of RatingsService class, a new one is created
            cls._appointments_DAO = AppointmentsDAO()
            cls._ratings_DAO = RatingsDAO()
            cls._users_DAO = UsersDAO()
            cls._notifications_DAO = NotificationsDAO()
            cls._dal_service = DALService()
            cls._instance = super(RatingsService, cls).__new__(cls)
        # There's already an instance of RatingsService class, so the existing one is returned
        return cls._instance

    def get_ratings(self, id_teacher):
        """
        Get rating by the rated id (teacher).
        :param: id_teacher: the user's id that gets a rating
        :return: list of ratings, If there's no ratings, it returns None
        """
        self._dal_service.start()
        try:
            user = self._users_DAO.get_user_by_id(id_teacher)
            if user is None:
                raise NotFoundException("User not found")
            all_ratings = self._ratings_DAO.get_ratings_from_teacher(id_teacher)
            for rating in all_ratings:
                rater = self._users_DAO.get_user_by_id(rating.id_rater)
                rating.setRater(rater)
            self._dal_service.commit_transaction()
            return all_ratings
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e

    def create_rating(self, rating):
        """
        Create a rating in the database.
        :param: rating: the rating to add
        :return: the rating added.
        """
        try:
            self._dal_service.start()
            if self._users_DAO.get_user_by_id(rating.id_rater) is None:
                raise NotFoundException("The student rater doesn't exist")
            if self._users_DAO.get_user_by_id(rating.id_rated) is None:
                raise NotFoundException("The teacher rater doesn't exist")
            # check if a finish appointment exist
            appointments = self._appointments_DAO.get_appointments_from_teacher_and_student(rating.id_rated,
                                                                                            rating.id_rater)
            if appointments is None:
                raise ForbiddenException("You have no course with this teacher")
            is_finished = False
            for appointment in appointments:
                if appointment.appointment_state == 'finished':
                    is_finished = True
            if not is_finished:
                raise ForbiddenException("You have not finished the course with this teacher")
            # check if a rating already exist
            rating_db = self._ratings_DAO.get_rating_by_id_rater_and_id_rated(rating.id_rater, rating.id_rated)
            if rating_db is not None:
                raise ConflictException("You already give this teacher a rating")
            rating = self._ratings_DAO.create_one_rating(rating)

            # add new notification
            user = self._users_DAO.get_user_by_id(rating.id_rater)

            self._notifications_DAO.add_notification(
                Notification(rating.id_rated, user.pseudo + " vous a ajouté un avis", None))

            self._dal_service.commit_transaction()
            return rating
        except Exception as e:
            self._dal_service.rollback_transaction()
            raise e
