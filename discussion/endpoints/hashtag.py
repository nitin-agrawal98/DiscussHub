from http import HTTPStatus

from flask import Blueprint, request

from middlewares.is_logged_in_user_for_discussion import is_logged_in_user_for_discussion
from middlewares.is_logged_in_user_for_hashtag import is_logged_in_user_for_hashtag
from query.hashtag import get_all_hashtags, get_hashtag_by_id, get_hashtag_by_tag, add_hashtag, \
    update_hashtag_properties
from utils.response import generate_response

hashtag_endpoints = Blueprint('hashtag_endpoints', __name__)


@hashtag_endpoints.route("", methods=["GET"])
def get_hashtags():
    try:
        hashtags = [hashtag.serialise() for hashtag in get_all_hashtags()]
        return generate_response(data=hashtags, status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@hashtag_endpoints.route("/<int:hashtag_id>", methods=["GET"])
def get_hashtag(hashtag_id):
    try:
        hashtag = get_hashtag_by_id(hashtag_id)
        if hashtag is None:
            return generate_response(message="Hashtag not found", status=HTTPStatus.NOT_FOUND)
        return generate_response(data=hashtag.serialise(), status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@hashtag_endpoints.route("", methods=["POST"])
def create_hashtag():
    try:
        json_content = request.json
        author_id = int(request.headers.get('X-User', -1))
        if author_id == -1:
            return generate_response(message="No logged in user", status=HTTPStatus.UNAUTHORIZED)
        tag = json_content.get('tag', None)
        if tag is None:
            return generate_response(message="Tag is required", status=HTTPStatus.BAD_REQUEST)
        hashtag_with_same_tag = get_hashtag_by_tag(tag)
        if hashtag_with_same_tag:
            return generate_response(message="Hashtag already exists", status=HTTPStatus.CONFLICT)
        json_content['author_id'] = author_id
        created_hashtag = add_hashtag(json_content)
        return generate_response(data=created_hashtag.serialise(), status=HTTPStatus.CREATED)
    except Exception as _:
        generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@hashtag_endpoints.route("/<int:hashtag_id>", methods=["PUT"])
@is_logged_in_user_for_hashtag
def update_hashtag(hashtag_id):
    try:
        existing_hashtag = get_hashtag_by_id(hashtag_id)
        if existing_hashtag is None:
            return generate_response(message=f'Hashtag with id {hashtag_id} not found', status=HTTPStatus.NOT_FOUND)
        updated_hashtag = request.json
        tag = updated_hashtag['tag'] or existing_hashtag['tag']
        hashtag_with_same_tag = get_hashtag_by_tag(tag)
        if hashtag_with_same_tag and not hashtag_with_same_tag.id == existing_hashtag.id:
            return generate_response(message='This tag already exists', status=HTTPStatus.CONFLICT)
        update_hashtag_properties(existing_hashtag, updated_hashtag)
        return generate_response(data=existing_hashtag.serialise(), status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
