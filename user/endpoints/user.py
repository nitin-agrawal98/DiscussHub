from http import HTTPStatus

from flask import Blueprint, request

from middlewares.is_logged_in_user import is_logged_in_user
from query import get_all_users, add_user, get_user_by_id, update_user_properties, get_user_by_email, \
    get_user_by_mobile, add_follow, get_follow, get_followers_of_followee, remove_all_users, get_followees_of_follower, \
    remove_follow
from utils.response import generate_response

user_endpoints = Blueprint("user_endpoints", __name__)


@user_endpoints.route("", methods=["GET"])
def get_users():
    try:
        users = [user.serialise() for user in get_all_users()]
        return generate_response(data=users, status=HTTPStatus.OK)
    except Exception as e:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@user_endpoints.route("/<int:user_id>", methods=["PUT"])
@is_logged_in_user
def update_user(user_id: int):
    try:
        existing_user = get_user_by_id(user_id)
        if existing_user is None:
            return generate_response(message=f'User with id {user_id} not found', status=HTTPStatus.NOT_FOUND)
        updated_user = request.json
        mobile = updated_user['mobile'] or existing_user['mobile']
        user_with_same_mobile = get_user_by_mobile(mobile)
        if user_with_same_mobile and not user_with_same_mobile.id == existing_user.id:
            return generate_response(message='This mobile already exists', status=HTTPStatus.CONFLICT)
        email = updated_user['email'] or existing_user['email']
        user_with_same_email = get_user_by_email(email)
        if user_with_same_email and not user_with_same_email.id == existing_user.id:
            return generate_response(message='This email already exists', status=HTTPStatus.CONFLICT)
        update_user_properties(existing_user, updated_user)
        return generate_response(data=existing_user.serialise(), status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@user_endpoints.route("", methods=["DELETE"])
def delete_users():
    try:
        remove_all_users()
        return generate_response(message="Deleted", status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@user_endpoints.route("/<int:followee_id>/follow", methods=["POST"])
def follow_user(followee_id):
    try:
        follower_id = int(request.headers.get('X-User', -1))
        if follower_id == -1:
            return generate_response(message="No logged in user", status=HTTPStatus.UNAUTHORIZED)
        if follower_id == followee_id:
            return generate_response(message="User can not follow themselves", status=HTTPStatus.BAD_REQUEST)
        follower = get_user_by_id(follower_id)
        if follower is None:
            return generate_response(message="Follower is not found", status=HTTPStatus.NOT_FOUND)
        followee = get_user_by_id(followee_id)
        if followee is None:
            return generate_response(message="Followee is not found", status=HTTPStatus.NOT_FOUND)
        follow = get_follow(follower_id, followee_id)
        if follow is not None:
            return generate_response(message="Follow relationship is already present", status=HTTPStatus.CONFLICT)
        created_follow = add_follow(followee_id, follower_id).serialise()
        return generate_response(data=created_follow, status=HTTPStatus.CREATED)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@user_endpoints.route("/<int:followee_id>/unfollow", methods=["DELETE"])
def unfollow_user(followee_id):
    try:
        follower_id = int(request.headers.get('X-User', -1))
        if follower_id == -1:
            return generate_response(message="No logged in user", status=HTTPStatus.UNAUTHORIZED)
        follow = get_follow(follower_id, followee_id)
        if follow is None:
            return generate_response(message="This follow relationship is not found", status=HTTPStatus.NOT_FOUND)
        remove_follow(follow)
        return generate_response(message="Unfollowed", status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@user_endpoints.route("/followers", methods=["GET"])
def get_followers():
    try:
        followee_id = int(request.headers.get('X-User', -1))
        if followee_id == -1:
            return generate_response(message="No logged in user", status=HTTPStatus.UNAUTHORIZED)
        followers = [follow.follower.serialise() for follow in get_followers_of_followee(followee_id)]
        return generate_response(data=followers, status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@user_endpoints.route("/followees", methods=["GET"])
def get_followees():
    try:
        follower_id = int(request.headers.get('X-User', -1))
        if follower_id == -1:
            return generate_response(message="No logged in user", status=HTTPStatus.UNAUTHORIZED)
        followees = [follow.followee.serialise() for follow in get_followees_of_follower(follower_id)]
        return generate_response(data=followees, status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
