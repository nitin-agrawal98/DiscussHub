from functools import wraps
from http import HTTPStatus

import jwt
from flask import request

from config import config
from utils.response import generate_response


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token:
            return generate_response(message='Token is missing', status=HTTPStatus.UNAUTHORIZED)

        try:
            data = jwt.decode(token, config['jwt']['secret_key'], algorithms=["HS256"])
            setattr(request, 'user_id', str(data['user']))
        except jwt.ExpiredSignatureError:
            return generate_response(message='Token has expired', status=HTTPStatus.UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return generate_response(message='Invalid token', status=HTTPStatus.UNAUTHORIZED)

        return f(*args, **kwargs)

    return decorated
