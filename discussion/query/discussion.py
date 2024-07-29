from database import session
from models.discussion_like import DiscussionLike
from models import DiscussionHashtag
from models.discussion import Discussion
from services.es.Discussion.discussion import discussionES


def get_all_discussions() -> list[Discussion]:
    return session.query(Discussion).all()


def get_all_discussions_by_author(author_id: int) -> list[Discussion]:
    return session.query(Discussion).filter_by(author_id=author_id).all()


def get_all_discussions_by_authors(author_ids: list[int]) -> list[Discussion]:
    return session.query(Discussion).filter(Discussion.author_id.in_(author_ids)).all()


def add_discussion(discussion_json: dict[str, str]) -> Discussion:
    try:
        discussion = Discussion(author_id=discussion_json.get('author_id'), text=discussion_json.get('text'),
                                image_url=discussion_json.get('image_url'))
        session.add(discussion)
        session.commit()
        discussionES.index(discussion)
        return discussion
    except:
        session.rollback()


def get_discussion_by_id(discussion_id: int) -> Discussion:
    return session.query(Discussion).get(discussion_id)


def update_discussion_properties(existing_discussion: Discussion, updated_discussion: dict[str, str]):
    try:
        existing_discussion.text = updated_discussion.get('text', existing_discussion.text)
        existing_discussion.image_url = updated_discussion.get('image_url', existing_discussion.image_url)
        session.commit()
        discussionES.index(existing_discussion)
    except:
        session.rollback()


def remove_discussion(discussion: Discussion):
    try:
        session.delete(discussion)
        session.commit()
        discussionES.delete_index(discussion)
    except:
        session.rollback()


def get_link_of_hashtag_to_discussion(discussion_id: int, hashtag_id: int) -> DiscussionHashtag:
    return session.query(DiscussionHashtag).filter_by(discussion_id=discussion_id, hashtag_id=hashtag_id).first()


def link_tag_to_discussion(discussion_id: int, hashtag_id: int) -> DiscussionHashtag:
    try:
        discussion_hashtag = DiscussionHashtag(discussion_id=discussion_id, hashtag_id=hashtag_id)
        session.add(discussion_hashtag)
        session.commit()
        discussionES.delete_index(discussion_hashtag.discussion)
        discussionES.index(discussion_hashtag.discussion)
        return discussion_hashtag
    except:
        session.rollback()


def unlink_tag_from_discussion(link: DiscussionHashtag):
    try:
        session.delete(link)
        session.commit()
        discussionES.delete_index(link.discussion)
        discussionES.index(link.discussion)
    except:
        session.rollback()


def get_discussion_like(author_id: int, discussion_id: int) -> DiscussionLike:
    return session.query(DiscussionLike).filter_by(author_id=author_id, discussion_id=discussion_id).first()


def add_like_to_discussion(author_id: int, discussion: Discussion):
    try:
        discussion_like = DiscussionLike(author_id=author_id, discussion_id=discussion.id)
        session.add(discussion_like)
        discussion.likes_count += 1
        discussionES.delete_index(discussion)
        discussionES.index(discussion)
        session.commit()
    except:
        session.rollback()


def remove_like_from_discussion(discussion_like: DiscussionLike, discussion: Discussion):
    try:
        session.delete(discussion_like)
        discussion.likes_count -= 1
        discussionES.delete_index(discussion)
        discussionES.index(discussion)
        session.commit()
    except:
        session.rollback()
