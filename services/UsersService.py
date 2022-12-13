import bcrypt
from flask import abort

from data.DAO.UsersDAO import UsersDAO
from data.services.DALService import DALService


class UsersService:
    users_DAO = UsersDAO()
    dal = DALService()

    def __init__(self):
        pass

    def get_users(self):
        self.dal.start()
        try:
            users = self.users_DAO.get_users()
            self.dal.commit_transaction()
            return users
        except Exception as e:
            self.dal.rollback_transaction()
            raise e

    def get_users_by_id(self, id):
        self.dal.start()
        try:
            user = self.users_DAO.get_user_by_id(id)
            if user is None:
                abort(404, "User not found")
            self.dal.commit_transaction()
            return user
        except Exception as e:
            self.dal.rollback_transaction()
            raise e

    def get_users_by_email(self, email):
        self.dal.start()
        try:
            user = self.users_DAO.get_user_by_email(email)
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
            user = self.users_DAO.get_user_by_pseudo(pseudo)
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
            user_email = self.users_DAO.get_user_by_email(user['email'])
            if user_email is not None:
                abort(409, "Cet email est déjà pris")
            user_pseudo = self.users_DAO.get_user_by_pseudo(user['pseudo'])
            if user_pseudo is not None:
                abort(409, "Ce pseudo est déjà pris")
            self.users_DAO.sing_in_user(user)
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
            user = self.users_DAO.get_user_by_id(token['id'])
            if user is None:
                abort(404, "User not found")
            self.dal.commit_transaction()
            return user
        except Exception as e:
            self.dal.rollback_transaction()
            raise e
