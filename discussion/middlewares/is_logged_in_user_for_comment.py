from functools import wraps
from http import HTTPStatus

from flask import request

from query.comment import get_comment_by_id
from utils.response import generate_response


def is_logged_in_user_for_comment(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = int(request.headers.get('X-User', -1))
        if user_id == -1:
            return generate_response(message="No logged in user", status=HTTPStatus.UNAUTHORIZED)
        comment_id = request.view_args['comment_id']
        comment = get_comment_by_id(comment_id)
        if comment is None:
            return generate_response(message="Comment not found", status=HTTPStatus.NOT_FOUND)
        if not user_id == int(comment.author_id):
            return generate_response(message="You do not have access for this", status=HTTPStatus.FORBIDDEN)
        return f(*args, **kwargs)

    return decorated
