from data.UsersDao import UsersDAO

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
        return self.users_DAO.getUserByEmail(email)

    def singInUser(self, user):

        password = user['password']
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user['password'] = hashed.decode()

        return self.users_DAO.singInUser(user)
