class ConflictException(Exception):
    def __init__(self, message=None):
        if message is None:
            message = "This object already exists, you can't add the same."
        super().__init__(self, message)
