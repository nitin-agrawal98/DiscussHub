from http import HTTPStatus

from flask import jsonify


def generate_response(status, data=None, message=None):
    if status == HTTPStatus.INTERNAL_SERVER_ERROR:
        return jsonify(message="Internal Server Error"), status
    return jsonify(data=data, message=message), status
