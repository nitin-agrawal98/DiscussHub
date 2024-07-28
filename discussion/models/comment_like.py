from sqlalchemy import Column, BIGINT, ForeignKey

from .base import Base


class CommentLike(Base):
    __tablename__ = 'comment_like'

    author_id = Column(BIGINT, primary_key=True)
    comment_id = Column(BIGINT, ForeignKey('discussion.id'), primary_key=True)

    def __repr__(self):
        return f'<DiscussionLike {self.author_id} {self.comment_id}>'

    def serialise(self):
        return {"id": self.id, "author_id": self.author_id, "comment_id": self.comment_id}
