class BadRequestException(Exception):
    def __init__(self, message=None):
        if message is None:
            message = "OH OH STOOOP, your request is not good, check it's correct before sending it to us :'("
        super().__init__(self, message)
