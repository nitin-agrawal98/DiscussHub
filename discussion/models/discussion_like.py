from sqlalchemy import Column, BIGINT, ForeignKey

from .base import Base


class DiscussionLike(Base):
    __tablename__ = 'discussion_like'

    author_id = Column(BIGINT, primary_key=True)
    discussion_id = Column(BIGINT, ForeignKey('discussion.id'), primary_key=True)

    def __repr__(self):
        return f'<DiscussionLike {self.author_id} {self.discussion_id}>'

    def serialise(self):
        return {"id": self.id, "author_id": self.author_id, "discussion_id": self.discussion_id}
