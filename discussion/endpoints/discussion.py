from http import HTTPStatus

from flask import Blueprint, request

from middlewares.is_logged_in_user_for_comment import is_logged_in_user_for_comment
from middlewares.is_logged_in_user_for_discussion import is_logged_in_user_for_discussion
from query.comment import add_comment, get_comment_by_id, remove_comment, update_comment_properties, get_comment_like, \
    add_like_to_comment, remove_like_from_comment, get_all_comments_by_discussion
from query.discussion import get_all_discussions_by_author, add_discussion, get_discussion_by_id, \
    update_discussion_properties, \
    remove_discussion, get_all_discussions_by_authors, link_tag_to_discussion, unlink_tag_from_discussion, \
    get_link_of_hashtag_to_discussion, add_like_to_discussion, get_discussion_like, remove_like_from_discussion, \
    get_likes_count_for_discussion
from query.hashtag import get_hashtag_by_tag, add_hashtag, get_hashtag_by_id
from services.es.Discussion.discussion import discussionES
from services.image_service import upload_image, delete_image, get_file_location
from utils.response import generate_response

discussion_endpoints = Blueprint('discussion_endpoints', __name__)


@discussion_endpoints.route("/authors", methods=["GET"])
def get_discussions_for_authors():
    try:
        author_ids = [int(author_id) for author_id in request.args.get('author_ids').split(',')]
        discussions = [discussion.serialise() for discussion in get_all_discussions_by_authors(author_ids)]
        return generate_response(data=discussions, status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/authors/<int:author_id>", methods=["GET"])
def get_discussions(author_id):
    try:
        discussions = [discussion.serialise() for discussion in get_all_discussions_by_author(author_id)]
        return generate_response(data=discussions, status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>", methods=["GET"])
def get_discussion(discussion_id):
    try:
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        return generate_response(data=discussion.serialise(), status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("", methods=["POST"])
def create_discussion():
    try:
        form_content = dict(request.form)
        text = form_content.get('text', None)
        author_id = request.headers.get('X-User', -1)
        if author_id == -1:
            return generate_response(message='No logged in user', status=HTTPStatus.UNAUTHORIZED)
        form_content['author_id'] = author_id
        if text is None:
            return generate_response(message='Text field is required', status=HTTPStatus.BAD_REQUEST)
        image = request.files.get('image', None)
        if image:
            file_location = get_file_location(author_id)
            image_url = upload_image(image, file_location)
            form_content['image_url'] = image_url
        created_user = add_discussion(form_content)
        return generate_response(data=created_user.serialise(), status=HTTPStatus.CREATED)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>", methods=["PUT"])
@is_logged_in_user_for_discussion
def update_discussion(discussion_id):
    try:
        existing_discussion = get_discussion_by_id(discussion_id)
        if existing_discussion is None:
            return generate_response(message='This discussion is not found', status=HTTPStatus.NOT_FOUND)
        updated_discussion = dict(request.form)
        image_url = existing_discussion.image_url
        image = request.files.get('image', None)
        if image_url:
            delete_image(image_url)
        if image:
            image_url = upload_image(image, get_file_location(existing_discussion.author_id))
            updated_discussion['image_url'] = image_url
        update_discussion_properties(existing_discussion, updated_discussion)
        return generate_response(data=existing_discussion.serialise(), status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>", methods=["DELETE"])
@is_logged_in_user_for_discussion
def delete_discussion(discussion_id):
    try:
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response("Discussion not found"), HTTPStatus.NOT_FOUND
        if discussion.image_url:
            delete_image(discussion.image_url)
        remove_discussion(discussion)
        return generate_response(message='Deleted', status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/search", methods=["GET"])
def search_discussion():
    try:
        text = request.args.get('text')
        hashtags = request.args.get('hashtags', [])
        if hashtags:
            hashtags = hashtags.split(',')
        data = discussionES.search({"query_text": text, "hashtags": hashtags})
        return generate_response(data=data, status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>/like", methods=["GET"])
def get_likes_of_discussion(discussion_id):
    try:
        user_id = int(request.headers.get('X-User'))
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        likes_count = get_likes_count_for_discussion(discussion_id)
        return generate_response(data=likes_count, status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>/like", methods=["POST"])
def like_discussion(discussion_id):
    try:
        user_id = int(request.headers.get('X-User'))
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        discussion_like = get_discussion_like(user_id, discussion_id)
        if discussion_like:
            return generate_response(message="User has already liked it", status=HTTPStatus.BAD_REQUEST)
        add_like_to_discussion(user_id, discussion)
        return generate_response(message="Liked", status=HTTPStatus.CREATED)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>/unlike", methods=["DELETE"])
def unlike_discussion(discussion_id):
    try:
        user_id = int(request.headers.get('X-User'))
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        discussion_like = get_discussion_like(user_id, discussion_id)
        if discussion_like is None:
            return generate_response(message="User has not liked it yet", status=HTTPStatus.BAD_REQUEST)
        remove_like_from_discussion(discussion_like, discussion)
        return generate_response(message="UnLiked", status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>/tags", methods=["POST"])
@is_logged_in_user_for_discussion
def add_tag_to_discussion(discussion_id):
    try:
        user_id = int(request.headers.get('X-User'))
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        tag = request.json.get('tag', None)
        if tag is None:
            return generate_response(message="Tag is required", status=HTTPStatus.BAD_REQUEST)
        hashtag = get_hashtag_by_tag(tag)
        if hashtag is None:
            hashtag = add_hashtag({'author_id': user_id, 'tag': tag})
        else:
            is_already_linked = any(hashtag.tag == tag for hashtag in discussion.hashtags)
            if is_already_linked:
                return generate_response(message="This tag is already linked to discussion", status=HTTPStatus.BAD_REQUEST)
        link = link_tag_to_discussion(discussion_id, hashtag.id)
        return generate_response(data=link.serialise(), status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>/tags/<int:tag_id>", methods=["DELETE"])
@is_logged_in_user_for_discussion
def remove_tag_to_discussion(discussion_id, tag_id):
    try:
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        hashtag = get_hashtag_by_id(tag_id)
        if hashtag is None:
            return generate_response(message="Tag not found", status=HTTPStatus.NOT_FOUND)
        link = get_link_of_hashtag_to_discussion(discussion_id, hashtag.id)
        if link is None:
            return generate_response(message="Hashtag not linked to discussion", status=HTTPStatus.BAD_REQUEST)
        unlink_tag_from_discussion(link)
        return generate_response(message="Tag removed", status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>/comments", methods=["GET"])
def get_comments_for_a_discussion(discussion_id):
    try:
        user_id = int(request.headers.get('X-User'))
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        comments = [comment.serialise() for comment in get_all_comments_by_discussion(discussion_id)]
        return generate_response(data=comments, status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>/comments", methods=["POST"])
def add_comment_to_discussion(discussion_id):
    try:
        user_id = int(request.headers.get('X-User'))
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        text = request.json.get('text', None)
        if text is None:
            return generate_response(message="Comment is required", status=HTTPStatus.BAD_REQUEST)
        comment = add_comment({'author_id': user_id, 'discussion_id': discussion_id, 'text': text})
        return generate_response(data=comment.serialise(), status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>/comments/<int:comment_id>", methods=["PUT"])
@is_logged_in_user_for_comment
def update_comment(discussion_id, comment_id):
    try:
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        existing_comment = get_comment_by_id(comment_id)
        if existing_comment is None:
            return generate_response(message="Comment not found", status=HTTPStatus.NOT_FOUND)
        if not existing_comment.discussion_id == discussion_id:
            return generate_response(message="Comment not linked to discussion", status=HTTPStatus.BAD_REQUEST)
        updated_comment = request.json
        update_comment_properties(existing_comment, updated_comment)
        return generate_response(data=existing_comment.serialise(), status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>/comments/<int:comment_id>", methods=["DELETE"])
@is_logged_in_user_for_comment
def delete_comment(discussion_id, comment_id):
    try:
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        comment = get_comment_by_id(comment_id)
        if comment is None:
            return generate_response(message="Comment not found", status=HTTPStatus.NOT_FOUND)
        if not comment.discussion_id == discussion_id:
            return generate_response(message="Comment not linked to discussion", status=HTTPStatus.BAD_REQUEST)
        remove_comment(comment)
        return generate_response(message="Comment removed", status=HTTPStatus.OK)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>/comments/<int:comment_id>/like", methods=["POST"])
def like_comment(discussion_id, comment_id):
    try:
        user_id = int(request.headers.get('X-User'))
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        comment = get_comment_by_id(comment_id)
        if comment is None:
            return generate_response(message="Comment not found", status=HTTPStatus.NOT_FOUND)
        if not comment.discussion_id == discussion_id:
            return generate_response(message="Comment not linked to discussion", status=HTTPStatus.BAD_REQUEST)
        comment_like = get_comment_like(user_id, comment_id)
        if comment_like:
            return generate_response(message="User has already liked it", status=HTTPStatus.BAD_REQUEST)
        add_like_to_comment(user_id, comment)
        return generate_response(message="Liked", status=HTTPStatus.CREATED)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


@discussion_endpoints.route("/<int:discussion_id>/comments/<int:comment_id>/unlike", methods=["DELETE"])
def unlike_comment(discussion_id, comment_id):
    try:
        user_id = int(request.headers.get('X-User'))
        discussion = get_discussion_by_id(discussion_id)
        if discussion is None:
            return generate_response(message="Discussion not found", status=HTTPStatus.NOT_FOUND)
        comment = get_comment_by_id(comment_id)
        if comment is None:
            return generate_response(message="Comment not found", status=HTTPStatus.NOT_FOUND)
        if not comment.discussion_id == discussion_id:
            return generate_response(message="Comment not linked to discussion", status=HTTPStatus.BAD_REQUEST)
        comment_like = get_comment_like(user_id, comment_id)
        if comment_like is None:
            return generate_response(message="User has not liked it yet", status=HTTPStatus.BAD_REQUEST)
        remove_like_from_comment(comment_like, comment)
        return generate_response(message="Unliked", status=HTTPStatus.CREATED)
    except Exception as _:
        return generate_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
