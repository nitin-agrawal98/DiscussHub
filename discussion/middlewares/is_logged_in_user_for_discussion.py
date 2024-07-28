from functools import wraps
from http import HTTPStatus

from flask import request

from query.discussion import get_discussion_by_id
from utils.response import generate_response


def is_logged_in_user_for_discussion(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = int(request.headers.get('X-User', -1))
        if user_id == -1:
            return generate_response(message="No logged in user", status=HTTPStatus.UNAUTHORIZED)
        discussion_id = request.view_args['discussion_id']
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        if not user_id == int(discussion.author_id):
            return generate_response(message="You do not have access for this", status=HTTPStatus.FORBIDDEN)
        return f(*args, **kwargs)

    return decorated
