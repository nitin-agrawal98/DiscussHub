from flask import Flask
from flask_cors import CORS

from database import init_db
from query.discussion import get_all_discussions
from endpoints.discussion import discussion_endpoints
from endpoints.hashtag import hashtag_endpoints
from services.es.Discussion.discussion import discussionES

API_ROOT = '/api'

app = Flask(__name__)
CORS(app, origins=["*"])

with app.app_context():
    init_db()

app.register_blueprint(discussion_endpoints, url_prefix=API_ROOT + '/discussions')
app.register_blueprint(hashtag_endpoints, url_prefix=API_ROOT + '/hashtags')

# Indexing all discussions at the start
discussions = get_all_discussions()
for discussion in discussions:
    discussionES.index(discussion)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
