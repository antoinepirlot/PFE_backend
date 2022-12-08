import data.database as database


class DALService:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def start(self):
        self.connection = database.initialiseConnection()
        self.cursor = self.connection.cursor()
        # TODO threads

    def commit(self, sql, values):
        # TODO threads
        self.cursor.execute(sql, values)
        self.connection.commit()
        results = self.cursor.fetchall()
        self.connection.close()
        return results

# TODO rollback
