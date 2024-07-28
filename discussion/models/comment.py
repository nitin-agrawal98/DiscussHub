from sqlalchemy import Column, BIGINT, DATETIME, TEXT, ForeignKey, INTEGER
from sqlalchemy.orm import relationship

from utils.time import get_current_time
from .base import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(BIGINT, primary_key=True)
    discussion_id = Column(BIGINT, ForeignKey('discussion.id'), nullable=False)
    author_id = Column(BIGINT, nullable=False)
    text = Column(TEXT)
    created_at = Column(DATETIME, default=get_current_time)
    parent_id = Column(BIGINT, ForeignKey('comment.id'), nullable=True)
    likes_count = Column(INTEGER, default=0)

    parent = relationship('Comment', remote_side=[id], back_populates='replies')
    replies = relationship('Comment', back_populates='parent', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Comment {self.id}>'

    def serialise(self):
        return {"id": self.id, "text": self.text, "author_id": self.author_id, 'replies': self.replies,
                'parent': self.parent, "likes_count": self.likes_count}
