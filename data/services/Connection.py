from threading import Thread


class Connection(Thread):
    def __init__(self, connection):
        super().__init__()
        self._connection = connection
        self._cursor = connection.cursor()

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor
