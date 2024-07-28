from functools import wraps
from http import HTTPStatus

from flask import request

from utils.response import generate_response


def is_logged_in_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = int(request.headers.get('X-User', None))
        if user_id is None:
            return generate_response(message="No logged in user", status=HTTPStatus.UNAUTHORIZED)
        if not user_id == int(request.view_args['user_id']):
            return generate_response(message="You do not have access for this", status=HTTPStatus.FORBIDDEN)
        return f(*args, **kwargs)

    return decorated
