from sqlalchemy import Column, BIGINT, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class DiscussionHashtag(Base):
    __tablename__ = 'discussion_hashtag'

    discussion_id = Column(BIGINT, ForeignKey('discussion.id'), primary_key=True)
    hashtag_id = Column(BIGINT, ForeignKey('hashtag.id'), primary_key=True)

    discussion = relationship('Discussion', foreign_keys='DiscussionHashtag.discussion_id')
    hashtag = relationship('Hashtag', foreign_keys='DiscussionHashtag.hashtag_id')

    def __repr__(self):
        return f'<DiscussionHashtag {self.discussion_id} {self.hashtag_id}>'

    def serialise(self):
        return {"discussion": self.discussion.serialise(), "hashtag": self.hashtag.serialise()}
