class UnauthorizedException(Exception):
    def __init__(self, message=None):
        if message is None:
            message = "You can't access this route, you're not allowed."
        super().__init__(self, message)
