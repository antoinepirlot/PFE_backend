from data.UsersDao import UsersDAO


class UsersService:
    users_DAO = UsersDAO()

    def __init__(self):
        pass

    def get_users(self):
        return self.users_DAO.get_users()
