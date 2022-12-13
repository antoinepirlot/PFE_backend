import bcrypt
from flask import abort

from Exceptions.WebExceptions.NotFoundException import NotFoundException
from data.DAO.CategoriesDAO import CategoriesDAO
from data.DAO.RatingsDAO import RatingsDAO
from data.DAO.UsersDAO import UsersDAO
from data.services.DALService import DALService


class UsersService:
    users_dao = UsersDAO()
    categories_dao = CategoriesDAO()
    ratings_dao = RatingsDAO()
    dal = DALService()

    def __init__(self):
        pass

    def get_users(self):
        self.dal.start()
        try:
            users = self.users_dao.get_users()
            self.dal.commit_transaction()
            return users
        except Exception as e:
            self.dal.rollback_transaction()
            raise e

    def get_users_by_id(self, id):
        self.dal.start()
        try:
            user = self.users_dao.get_user_by_id(id)
            if user is None:
                abort(404, "User not found")
            self.dal.commit_transaction()
            return user
        except Exception as e:
            self.dal.rollback_transaction()
            raise e

    def get_teacher_by_id(self, id):
        '''
        Get a user with its average rating and its categories
        :param id: id of the user
        :return: the user retrieved
        '''
        self.dal.start()
        try:
            user = self.users_dao.get_user_by_id(id)
            if user is None:
                raise NotFoundException("User not found")
            all_skills = self.categories_dao.get_all_skills_categories(id)
            user.skills = all_skills
            all_ratings = self.ratings_dao.get_ratings_from_teacher(id)
            if len(all_ratings) != 0:
                all_ratings_counter = 0
                for rating in all_ratings:
                    all_ratings_counter += rating.rating_number
                user.average_rating = (all_ratings_counter/len(all_ratings))
            self.dal.commit_transaction()
            return user
        except Exception as e:
            self.dal.rollback_transaction()
            raise e



    def get_users_by_email(self, email):
        self.dal.start()
        try:
            user = self.users_dao.get_user_by_email(email)
            if user is None:
                abort(404, "User not found")
            self.dal.commit_transaction()
            return user
        except Exception as e:
            self.dal.rollback_transaction()
            raise e

    def get_users_by_pseudo(self, pseudo):
        self.dal.start()
        try:
            user = self.users_dao.get_user_by_pseudo(pseudo)
            if user is None:
                abort(404, "User not found")
            self.dal.commit_transaction()
            return user
        except Exception as e:
            self.dal.rollback_transaction()
            raise e

    def sing_in_user(self, user):
        password = user['password']
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user['password'] = hashed.decode()
        self.dal.start()
        try:
            user_email = self.users_dao.get_user_by_email(user['email'])
            if user_email is not None:
                abort(409, "Cet email est déjà pris")
            user_pseudo = self.users_dao.get_user_by_pseudo(user['pseudo'])
            if user_pseudo is not None:
                abort(409, "Ce pseudo est déjà pris")
            self.users_dao.sing_in_user(user)
            self.dal.commit_transaction()
        except Exception as e:
            self.dal.rollback_transaction()
            raise e

    def logInUser(self, email, password):

        userFound = self.get_users_by_email(email).convert_to_json()

        if not bcrypt.checkpw(password.encode(), userFound['password'].encode()):
            abort(404, "Email or password incorrect")

        return userFound

    def get_users_by_token(self, token):
        self.dal.start()
        try:
            user = self.users_dao.get_user_by_id(token['id'])
            if user is None:
                abort(404, "User not found")
            self.dal.commit_transaction()
            return user
        except Exception as e:
            self.dal.rollback_transaction()
            raise e
