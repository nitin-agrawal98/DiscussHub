from http import HTTPStatus

from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash

from query import get_user_by_mobile, get_user_by_email, add_user
from utils.response import generate_response

auth_endpoints = Blueprint("auth_endpoints", __name__)


@auth_endpoints.route("/signup", methods=["POST"])
def signup():
    try:
        json_content = request.json
        name = json_content.get('name', None)
        email = json_content.get('email', None)
        mobile = json_content.get('mobile', None)
        password = json_content.get('password', None)
        if None in [name, email, mobile, password]:
            return generate_response(message='Missing Parameters', status=HTTPStatus.BAD_REQUEST)
        user_with_same_mobile = get_user_by_mobile(mobile)
        if user_with_same_mobile is not None:
            return generate_response(message='This mobile already exists', status=HTTPStatus.CONFLICT)
        user_with_same_email = get_user_by_email(email)
        if user_with_same_email is not None:
            return generate_response(message='This email already exists', status=HTTPStatus.CONFLICT)
        json_content['password'] = generate_password_hash(password)
        created_user = add_user(json_content)
        return generate_response(data=created_user.serialise(), status=HTTPStatus.CREATED)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@auth_endpoints.route("/login", methods=["POST"])
def login():
    try:
        auth = request.authorization
        username = auth.get('username', None)
        password = auth.get('password', None)
        if None in [username, password]:
            return generate_response(message="Username and password are required", status=HTTPStatus.BAD_REQUEST)
        user = get_user_by_email(username) or get_user_by_mobile(username)
        if user and check_password_hash(user.password, password):
            return generate_response(data={"user_id": user.id}, status=HTTPStatus.OK)
        return generate_response(message="username or password invalid", status=HTTPStatus.UNAUTHORIZED)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
