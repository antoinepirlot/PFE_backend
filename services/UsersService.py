import bcrypt
from flask import abort

from Exceptions.WebExceptions.ConflictException import ConflictException
from Exceptions.WebExceptions.NotFoundException import NotFoundException
from data.DAO.CategoriesDAO import CategoriesDAO
from data.DAO.RatingsDAO import RatingsDAO
from data.DAO.UsersDAO import UsersDAO
from data.services.DALService import DALService


class UsersService:
    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of DALService class, a new one is created
            cls._users_dao = UsersDAO()
            cls._categories_dao = CategoriesDAO()
            cls._ratings_dao = RatingsDAO()
            cls._dal = DALService()
            cls._instance = super(UsersService, cls).__new__(cls)
        # There's already an instance of DALService class, so the existing one is returned
        return cls._instance

    def get_users(self):
        """
        Get all users, from database.
        :return: the list of users
        """
        self._dal.start()
        try:
            users = self._users_dao.get_users()
            self._dal.commit_transaction()
            return users
        except Exception as e:
            self._dal.rollback_transaction()
            raise e

    def get_users_by_id(self, id):
        """
        Get user by his id .
        :param: id_user: the user's id
        :return: the user, If there's no user, it returns None
        """
        self._dal.start()
        try:
            user = self._users_dao.get_user_by_id(id)
            if user is None:
                abort(404, "User not found")
            self._dal.commit_transaction()
            return user
        except Exception as e:
            self._dal.rollback_transaction()
            raise e

    def get_teacher_by_id(self, id):
        """
        Get a user with its average rating and its categories
        :param id: id of the user
        :return: the user retrieved
        """
        self._dal.start()
        try:
            user = self._users_dao.get_user_by_id(id)
            if user is None:
                raise NotFoundException("User not found")
            all_skills = self._categories_dao.get_all_skills_categories(id)
            user.skills = all_skills
            all_ratings = self._ratings_dao.get_ratings_from_teacher(id)
            if len(all_ratings) != 0:
                all_ratings_counter = 0
                for rating in all_ratings:
                    all_ratings_counter += rating.rating_number
                user.average_rating = (all_ratings_counter / len(all_ratings))
            self._dal.commit_transaction()
            return user
        except Exception as e:
            self._dal.rollback_transaction()
            raise e

    def get_users_by_email(self, email):
        """
        Get user by his email .
        :param: email: the user's email
        :return: the user, If there's no user, it returns None
        """
        self._dal.start()
        try:
            user = self._users_dao.get_user_by_email(email)
            if user is None:
                raise NotFoundException("User not found")
            self._dal.commit_transaction()
            return user
        except Exception as e:
            self._dal.rollback_transaction()
            raise e

    def get_users_by_pseudo(self, pseudo):
        """
        Get user by his pseudo .
        :param: pseudo: the user's pseudo
        :return: the user, If there's no user, it returns None
        """
        self._dal.start()
        try:
            user = self._users_dao.get_user_by_pseudo(pseudo)
            if user is None:
                raise NotFoundException("User not found")
            self._dal.commit_transaction()
            return user
        except Exception as e:
            self._dal.rollback_transaction()
            raise e

    def sing_in_user(self, user):
        """
        Create a user in the database.
        :param: user: the user to add
        """

        password = user['password']
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user['password'] = hashed.decode()
        self._dal.start()
        try:
            user_email = self._users_dao.get_user_by_email(user['email'])
            if user_email is not None:
                raise ConflictException("Cet email est déjà pris")
            user_pseudo = self._users_dao.get_user_by_pseudo(user['pseudo'])
            if user_pseudo is not None:
                raise ConflictException("Ce pseudo est déjà pris")
            self._users_dao.sing_in_user(user)
            self._dal.commit_transaction()
        except Exception as e:
            self._dal.rollback_transaction()
            raise e

    def logInUser(self, email, password):
        """
        Login a user.
        :param: email: the user's email.
        :param: password: the user's email.
        :return: the user found.
        """

        userFound = self.get_users_by_email(email).convert_to_json()

        if not bcrypt.checkpw(password.encode(), userFound['password'].encode()):
            raise NotFoundException("Email or password incorrect")

        return userFound

    def get_users_by_token(self, token):
        """
        Get user by his token .
        :param: token: the user's token
        :return: the user, If there's no user, it returns None
        """
        self._dal.start()
        try:
            user = self._users_dao.get_user_by_id(token['id'])
            if user is None:
                raise NotFoundException("User not found")
            self._dal.commit_transaction()
            return user
        except Exception as e:
            self._dal.rollback_transaction()
            raise e
