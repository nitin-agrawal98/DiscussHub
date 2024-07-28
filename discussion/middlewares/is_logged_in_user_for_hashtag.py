from functools import wraps
from http import HTTPStatus

from flask import request

from query.hashtag import get_hashtag_by_id
from utils.response import generate_response


def is_logged_in_user_for_hashtag(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = int(request.headers.get('X-User', -1))
        if user_id == -1:
            return generate_response(message="No logged in user", status=HTTPStatus.UNAUTHORIZED)
        hashtag_id = request.view_args['hashtag_id']
        hashtag = get_hashtag_by_id(hashtag_id)
        if hashtag is None:
            return generate_response(message="Hashtag not found", status=HTTPStatus.NOT_FOUND)
        if not user_id == int(hashtag.author_id):
            return generate_response(message="You do not have access for this", status=HTTPStatus.FORBIDDEN)
        return f(*args, **kwargs)

    return decorated
