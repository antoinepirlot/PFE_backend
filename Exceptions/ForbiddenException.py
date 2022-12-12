class ForbiddenException(Exception):
    def __init__(self, message=None):
        if message is None:
            message = "Who are you? You can't do it, try to log in, maybe you can? :o"
        super().__init__(self, message)
