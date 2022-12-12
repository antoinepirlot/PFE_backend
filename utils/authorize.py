from functools import wraps
from flask import request, jsonify, make_response
import jwt
import os
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
            return jsonify("A valid token is missing!"), 401
        try:
            # decode the token to check if the user exists
            data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=['HS256'])
            users_service.get_users_by_id(data['id'])
        except:  # the token is invalid
            return jsonify("Invalid token!"), 403
        return f(*args, **kwargs)

    return decorator
