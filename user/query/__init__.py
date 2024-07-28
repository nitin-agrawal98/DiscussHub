from database import session
from models import User, Follow


def get_all_users() -> list[User]:
    return session.query(User).all()


def add_user(user_json: User) -> User:
    user = User(name=user_json.get('name'), email=user_json.get('email'), mobile=user_json.get('mobile'), password=user_json.get('password'))
    session.add(user)
    session.commit()
    return user


def get_user_by_id(user_id: int) -> User:
    return session.query(User).get(user_id)


def get_user_by_mobile(mobile: str) -> User:
    return session.query(User).filter_by(mobile=mobile).first()


def get_user_by_email(email: str) -> User:
    return session.query(User).filter_by(email=email).first()


def update_user_properties(existing_user: User, updated_user: dict[str, str]):
    existing_user.name = updated_user.get('name', existing_user.name)
    existing_user.email = updated_user.get('email', existing_user.email)
    existing_user.mobile = updated_user.get('mobile', existing_user.mobile)
    session.commit()


def remove_all_users():
    session.query(User).delete()
    session.commit()


def add_follow(followee_id: int, follower_id: int) -> Follow:
    follow = Follow(follower_id=follower_id, followee_id=followee_id)
    session.add(follow)
    session.commit()
    return follow


def get_follow(follower_id: int, followee_id: int) -> Follow:
    return session.query(Follow).filter_by(follower_id=follower_id, followee_id=followee_id).first()


def get_followers_of_followee(followee_id: int) -> list[Follow]:
    return session.query(Follow).filter_by(followee_id=followee_id).all()


def get_followees_of_follower(follower_id: int) -> list[Follow]:
    return session.query(Follow).filter_by(follower_id=follower_id).all()


def remove_follow(follow: Follow):
    session.delete(follow)
    session.commit()
