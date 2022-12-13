import os
from functools import wraps

import jwt
from flask import request

from Exceptions.WebExceptions.BadRequestException import BadRequestException
from Exceptions.WebExceptions.ForbiddenException import ForbiddenException
from services.UsersService import UsersService

users_service = UsersService()


# Authorize decorator
def authorize(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # check if token passed
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:  # if not token
            raise BadRequestException("A valid token is missing!")
        get_id_from_token(token)
        return f(*args, **kwargs)

    return decorator


def get_id_from_token(token):
    try:
        # decode the token to check if the user exists
        data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=['HS256'])
        users_service.get_users_by_id(data['id'])
    except Exception:  # the token is invalid
        raise ForbiddenException("Invalid token!")
