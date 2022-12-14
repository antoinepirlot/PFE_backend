import threading

import psycopg2

import data.database as database
from Exceptions.FatalException import FatalException


class DALService:

    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            # No instance of DALService class, a new one is created
            cls._instance = super(DALService, cls).__new__(cls)
            cls._pool = database.initialiseConnection()
            cls._connectionsStorage = threading.local()
        # There's already an instance of DALService class, so the existing one is returned
        return cls._instance

    def start(self):
        """
        Start a transaction by getting a connexion
        :return: FatalException if a problem occurs
        """
        try:
            self._connectionsStorage.connection = self._pool.getconn()
            self._connectionsStorage.connection.autocommit = False
        except Exception:
            raise FatalException

    def commit_transaction(self):
        """
        Commit the current transaction
        :return: FatalException if a problem occurs
        """
        try:
            connection = self._connectionsStorage.connection
            connection.commit()
            connection.cursor().close()
            self._pool.putconn(self._connectionsStorage.connection)
            self._connectionsStorage.connection = None
        except Exception:
            raise FatalException

    def execute(self, sql, values, fetch=False):
        """
        Execute a sql query with or without fetching thanks to the current transaction
        :param sql: the sql query
        :param values: the dictionary that enuma
        :param fetch: a boolean that represents if you need to fetch or not
        :return: the result or FatalException if a problem occurs or nothing
        """
        try:
            connection = self._connectionsStorage.connection
            cursor = connection.cursor()
            cursor.execute(sql, values)
            if fetch:
                results = cursor.fetchall()
                return results
        except psycopg2.DatabaseError as e:
            try:
                print("SQL Error [%d]: %s" % (e.args[0], e.args[1]))
                raise FatalException
            except IndexError:
                print("SQL Error: %s" % str(e))
                raise FatalException
        except Exception:
            raise FatalException

    def rollback_transaction(self):
        """
        Rollback the current transaction
        :return: FatalException if a problem occurs
        """
        try:
            connection = self._connectionsStorage.connection
            connection.rollback()
            cursor = connection.cursor()
            cursor.close()
            self._pool.putconn(self._connectionsStorage.connection)
            self._connectionsStorage.connection = None
        except Exception:
            raise FatalException
