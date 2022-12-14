import psycopg2

from data.services.DALService import DALService
from models.User import User


class UsersDAO:
    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of DALService class, a new one is created
            cls._dal = DALService()
            cls._instance = super(UsersDAO, cls).__new__(cls)
        # There's already an instance of DALService class, so the existing one is returned
        return cls._instance

    def get_users(self):
        """
        Get all users, from database.
        :return: the list of users
        """
        sql = """SELECT id_user, lastname, firstname, email, pseudo, sexe, phone, password FROM projet.users"""

        resultsExportUsers = []
        results = self._dal.execute(sql, None, True)

        for row in results:
            user = User(int(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]),
                        str(row[7]))
            resultsExportUsers.append(user)
        return resultsExportUsers

    def get_user_by_id(self, id_user):
        """
        Get user by his id .
        :param: id_user: the user's id
        :return: the user, If there's no user, it returns None
        """
        sql = """SELECT id_user, lastname, firstname, email, pseudo, sexe, phone, password
                  FROM projet.users 
                  WHERE id_user = %(id_user)s;
                  """

        value = {"id_user": id_user}
        result = self._dal.execute(sql, value, True)
        if len(result) == 0:
            return None
        result = result[0]
        user = User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
        return user

    def get_user_by_email(self, email):
        """
        Get user by his email .
        :param: email: the user's email
        :return: the user, If there's no user, it returns None
        """
        sql = """SELECT id_user, lastname, firstname, email, pseudo, sexe, phone, password
                          FROM projet.users 
                          WHERE email = %(email)s;
                          """

        value = {"email": email}
        result = self._dal.execute(sql, value, True)
        if len(result) == 0:
            return None
        result = result[0]
        user = User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
        return user

    def get_user_by_pseudo(self, pseudo):
        """
        Get user by his pseudo .
        :param: pseudo: the user's pseudo
        :return: the user, If there's no user, it returns None
        """
        sql = """SELECT id_user, lastname, firstname, email, pseudo, sexe, phone, password
                              FROM projet.users 
                              WHERE pseudo = %(pseudo)s;
                              """

        value = {"pseudo": pseudo}
        result = self._dal.execute(sql, value, True)
        if len(result) == 0:
            return None
        result = result[0]
        user = User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
        return user

    def sing_in_user(self, user):
        """
        Create a user in the database.
        :param: user: the user to add
        """
        sql = "INSERT INTO projet.users VALUES (DEFAULT,'%s','%s','%s','%s','%s','%s','%s')" % (
            user['lastname'], user['firstname'], user['email'], user['pseudo'], user['sexe'], user['phone'],
            user['password'])

        self._dal.execute(sql, None)
