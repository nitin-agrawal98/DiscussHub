from sqlalchemy import Column, BIGINT, ForeignKey, DATETIME
from sqlalchemy.orm import relationship

from utils.time import get_current_time
from .base import Base


class Follow(Base):
    __tablename__ = 'follow'

    follower_id = Column(BIGINT, ForeignKey('user.id'), primary_key=True)
    followee_id = Column(BIGINT, ForeignKey('user.id'), primary_key=True)
    created_at = Column(DATETIME, default=get_current_time)

    follower = relationship('User', foreign_keys='Follow.follower_id')
    followee = relationship('User', foreign_keys='Follow.followee_id')

    def __repr__(self):
        return f'<User {self.email}>'

    def serialise(self):
        return {"follower": self.follower.serialise(), "followee": self.followee.serialise()}
