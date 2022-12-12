class NotFoundException(Exception):
    def __init__(self, message=None):
        if message is None:
            message = "Object(s) Not Found"
        super().__init__(self, message)
