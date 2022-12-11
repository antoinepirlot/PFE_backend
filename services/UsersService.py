from data.UsersDAO import UsersDAO
from flask import abort
from werkzeug.exceptions import NotFound

import bcrypt

from data.services.DALService import DALService


class UsersService:
    users_DAO = UsersDAO()
    dal = DALService()

    def __init__(self):
        pass

    def get_users(self):
        self.dal.start()
        users = self.users_DAO.get_users()
        self.dal.commit_transaction()
        return users

    def get_users_by_id(self, id):
        self.dal.start()
        user = self.users_DAO.get_user_by_id(id)
        if user is None:
            self.dal.rollback_transaction()
            abort(404, "User not found")
        self.dal.commit_transaction()
        return user

    def get_users_by_email(self, email):
        self.dal.start()
        user = self.users_DAO.get_user_by_email(email)
        if user is None:
            self.dal.rollback_transaction()
            abort(404, "User not found")
        self.dal.commit_transaction()
        return user

    def get_users_by_pseudo(self, pseudo):
        self.dal.start()
        user = self.users_DAO.get_user_by_pseudo(pseudo)
        if user is None:
            self.dal.rollback_transaction()
            abort(404, "User not found")
        self.dal.commit_transaction()
        return user

    def sing_in_user(self, user):
        password = user['password']
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user['password'] = hashed.decode()
        self.dal.start()
        user_created = None
        try:
            user_email = self.users_DAO.get_user_by_email(user['email'])
            if user_email is not None:
                self.dal.rollback_transaction()
                abort(409, "Cet email est déjà pris")
            user_pseudo = self.users_DAO.get_user_by_pseudo(user['pseudo'])
            if user_pseudo is not None:
                self.dal.rollback_transaction()
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
