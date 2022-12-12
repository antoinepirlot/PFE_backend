import data.database as database
import threading


class DALService:

    def __init__(self):
        pass

    def __new__(cls):
        if not hasattr(cls, "instance"):
            # No instance of DALService class, a new one is created
            cls.instance = super(DALService, cls).__new__(cls)
            cls.pool = database.initialiseConnection()
            cls.connectionsStorage = threading.local()
        # There's already an instance of DALService class, so the existing one is returned
        return cls.instance

    def start(self):
        self.connectionsStorage.connection = self.pool.getconn()
        self.connectionsStorage.connection.autocommit = False

    def commit_transaction(self):
        connection = self.connectionsStorage.connection
        connection.commit()
        connection.cursor().close()
        self.pool.putconn(self.connectionsStorage.connection)
        self.connectionsStorage.connection = None

    def execute(self, sql, values, fetch=False):
        connection = self.connectionsStorage.connection
        cursor = connection.cursor()
        cursor.execute(sql, values)
        if fetch:
            results = cursor.fetchall()
            return results

    def rollback_transaction(self):
        connection = self.connectionsStorage.connection
        connection.rollback()
        cursor = connection.cursor()
        cursor.close()
        self.pool.putconn(self.connectionsStorage.connection)
        self.connectionsStorage.connection = None
