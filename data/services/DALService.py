import data.database as database


class DALService:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            # No instance of DALService class, a new one is created
            cls.instance = super(DALService, cls).__new__(cls)
        # There's already an instance of DALService class, so the existing one is returned
        return cls.instance

    def start(self):
        self.connection = database.initialiseConnection()
        self.cursor = self.connection.cursor()
        # TODO threads

    def commit(self, sql, values): #TODO : delete this function
        # TODO threads
        self.cursor.execute(sql, values)
        self.connection.commit()
        results = self.cursor.fetchall()
        self.cursor.close()
        self.connection.close()
        return results

    def commit_transaction(self):
        # TODO threads
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def execute(self, sql, values, fetch=False):
        self.cursor.execute(sql, values)
        if fetch:
            results = self.cursor.fetchall()
            return results

    def rollback_transaction(self):
        self.connection.rollback()
        self.cursor.close()
        self.connection.close()

# TODO rollback
