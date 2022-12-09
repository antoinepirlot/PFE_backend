from data.UsersDao import UsersDAO
from flask import abort

import bcrypt

class UsersService:
    users_DAO = UsersDAO()

    def __init__(self):
        pass

    def get_users(self):
        return self.users_DAO.getUsers()

    def get_users_by_id(self, id):
        return self.users_DAO.getUserById(id)

    def get_users_by_email(self, email):
        user = self.users_DAO.getUserByEmail(email)
        if user is None:
            abort(404, "User not found")
        return user

    def singInUser(self, user):

        password = user['password']
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user['password'] = hashed.decode()

        return self.users_DAO.singInUser(user)

    def logInUser(self, email, password):

        userFound = self.get_users_by_email(email).convert_to_json()

        if not bcrypt.checkpw(password.encode(), userFound['password'].encode()):
            abort(404, "Email or password incorrect")

        return userFound