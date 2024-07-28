from database import session
from models import Hashtag


def get_all_hashtags() -> list[Hashtag]:
    return session.query(Hashtag).all()


def get_hashtag_by_id(hashtag_id: int) -> Hashtag:
    return session.query(Hashtag).get(hashtag_id)


def get_hashtag_by_tag(tag: str) -> Hashtag:
    return session.query(Hashtag).filter_by(tag=tag).first()


def add_hashtag(hashtag_json: dict[str, str]) -> Hashtag:
    try:
        hashtag = Hashtag(author_id=hashtag_json.get('author_id'), tag=hashtag_json.get('tag'))
        session.add(hashtag)
        session.commit()
        return hashtag
    except:
        session.rollback()


def update_hashtag_properties(existing_hashtag: Hashtag, updated_hashtag: dict[str, str]):
    try:
        existing_hashtag.tag = updated_hashtag.get('tag', existing_hashtag.tag)
        session.commit()
    except:
        session.rollback()
