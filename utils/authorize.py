from functools import wraps
from flask import jsonify, request
import jwt
import os
from services.UsersService import UsersService

users_service = UsersService()


# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:  # throw error if no token provided
            return "A valid token is missing!", 401
        try:
            # decode the token to obtain user id
            data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=['HS256'])
            current_user = UsersService.get_users_by_id(data['id'])
        except:
            return "Invalid token!", 401
        # Return the user information attached to the token
        return f(current_user, *args, **kwargs)

    return decorator
