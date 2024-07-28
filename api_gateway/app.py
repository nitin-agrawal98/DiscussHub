import datetime
import json
from http import HTTPStatus

import jwt
import requests
from flask import Flask, request
from flask_cors import CORS

from config import config
from middlewares.token_required import token_required
from utils.response import generate_response

app = Flask(__name__)
CORS(app, origins=["*"])


@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if auth:
        response = requests.post(
            'http://localhost:5001/api/login',
            auth=(auth.username, auth.password)
        )
        data = json.loads(response.content).get('data')
        if data is None or data.get('user_id') is None:
            return generate_response(message="Invalid username or password", status=HTTPStatus.UNAUTHORIZED)
        access_expires_on = datetime.datetime.utcnow() + config['jwt']['access_token_expires']
        access_token = jwt.encode(
            {'user': data['user_id'], 'exp': access_expires_on},
            config['jwt']['secret_key'])
        refresh_expires_on = datetime.datetime.utcnow() + config['jwt']['refresh_token_expires']
        refresh_token = jwt.encode(
            {'user': data['user_id'], 'exp': refresh_expires_on},
            config['jwt']['secret_key'])
        return generate_response(data={"access_token": access_token, "refresh_token": refresh_token,
                                       "access_expires_on": access_expires_on, "refresh_expires_on": refresh_expires_on},
                                 status=HTTPStatus.OK)
    return generate_response(message='username and password are required', status=HTTPStatus.UNAUTHORIZED)


@app.route("/refresh-token", methods=["POST"])
@token_required
def refresh_access_token():
    try:
        user_id = request.user_id
        refresh_token = request.json.get('refresh_token', None)
        if refresh_token is None:
            return generate_response(message="Missing refresh token", status=HTTPStatus.BAD_REQUEST)
        data = jwt.decode(refresh_token, config['jwt']['secret_key'], algorithms=["HS256"])
        if user_id != int(data['user']):
            return generate_response(message="Invalid token", status=HTTPStatus.UNAUTHORIZED)
        access_expires_on = datetime.datetime.utcnow() + config['jwt']['access_token_expires']
        access_token = jwt.encode(
            {'user': user_id, 'exp': access_expires_on},
            config['jwt']['secret_key'])
        return generate_response(data={"access_token": access_token, "refresh_token": refresh_token,
                                       "access_expires_on": access_expires_on, "refresh_expires_on": data['exp']},
                                 status=HTTPStatus.OK)
    except jwt.ExpiredSignatureError:
        return generate_response(message="Token expired", status=HTTPStatus.UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return generate_response(message="Invalid token", status=HTTPStatus.UNAUTHORIZED)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route('/signup', methods=['POST'])
def signup():
    response = requests.request(
        method=request.method,
        url='http://localhost:5001/api/signup',
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    return response.content, response.status_code, response.headers.items()


@app.route('/user-service/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def user_service(path):
    url = f'{config["services"]["user_service"]}/{path}'
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    headers['X-User'] = request.user_id
    response = requests.request(
        method=request.method,
        url=url,
        params=request.args.to_dict(),
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    return response.content, response.status_code, response.headers.items()


@app.route('/discussion-service/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def discussion_service(path):
    url = f'{config["services"]["discussion_service"]}/{path}'
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    headers['X-User'] = request.user_id
    response = requests.request(
        method=request.method,
        url=url,
        params=request.args.to_dict(),
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    return response.content, response.status_code, response.headers.items()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
