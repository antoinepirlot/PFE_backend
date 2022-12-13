class FatalException(Exception, BaseException):
    def __init__(self, message=None):
        if message is None:
            message = "FatalException"
        super().__init__(self, message)
