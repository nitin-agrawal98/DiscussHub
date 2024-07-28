from database import session
from models import Comment, CommentLike


def get_all_comments_by_discussion(discussion_id: int) -> list[Comment]:
    return session.query(Comment).filter_by(discussion_id=discussion_id).all()


def get_comment_by_id(comment_id: int) -> Comment:
    return session.query(Comment).get(comment_id)


def add_comment(comment_json: dict[str, str]) -> Comment:
    try:
        comment = Comment(author_id=comment_json.get('author_id'), text=comment_json.get('text'),
                          discussion_id=comment_json.get('discussion_id'))
        session.add(comment)
        session.commit()
        return comment
    except:
        session.rollback()


def update_comment_properties(existing_comment: Comment, updated_comment: dict[str, str]):
    try:
        existing_comment.text = updated_comment.get('text', existing_comment.text)
        session.commit()
    except:
        session.rollback()


def remove_comment(comment: Comment):
    try:
        session.delete(comment)
        session.commit()
    except:
        session.rollback()


def get_comment_like(author_id: int, comment_id: int) -> CommentLike:
    return session.query(CommentLike).filter_by(author_id=author_id, comment_id=comment_id).first()


def add_like_to_comment(author_id: int, comment: Comment):
    try:
        comment_like = CommentLike(author_id=author_id, comment_id=comment.id)
        session.add(comment_like)
        comment.likes_count += 1
        session.commit()
    except:
        session.rollback()


def remove_like_from_comment(comment_like: CommentLike, comment: Comment):
    try:
        session.delete(comment_like)
        comment.likes_count -= 1
        session.commit()
    except:
        session.rollback()

