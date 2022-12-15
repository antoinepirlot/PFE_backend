import os
from datetime import datetime, timedelta

import jwt


def get_good_token(id):
    """
    Create a good token
    :return: the token
    """
    payload_data = {
        "id": id,
        'exp': datetime.utcnow() + timedelta(days=5)  # expiration time
    }
    my_secret = os.getenv("JWT_SECRET")
    token = jwt.encode(
        payload=payload_data,
        key=my_secret, algorithm="HS256"
    )
    return token