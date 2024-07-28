from flask import Flask, jsonify
from flask_cors import CORS

from database import init_db
from endpoints.auth import auth_endpoints
from endpoints.user import user_endpoints

API_ROOT = '/api'

app = Flask(__name__)
CORS(app, origins=["*"])

with app.app_context():
    init_db()

app.register_blueprint(auth_endpoints, url_prefix=API_ROOT)
app.register_blueprint(user_endpoints, url_prefix=API_ROOT + '/users')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
