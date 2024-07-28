from sqlalchemy import Column, BIGINT, DATETIME, TEXT, String, INTEGER
from sqlalchemy.orm import relationship

from utils.time import get_current_time
from .base import Base


class Discussion(Base):
    __tablename__ = 'discussion'

    id = Column(BIGINT, primary_key=True)
    author_id = Column(BIGINT, nullable=False)
    text = Column(TEXT, nullable=False)
    image_url = Column(String(200), nullable=True)
    created_at = Column(DATETIME, default=get_current_time)
    updated_at = Column(DATETIME, default=get_current_time, onupdate=get_current_time)
    likes_count = Column(INTEGER, default=0)

    hashtags = relationship('Hashtag', secondary='discussion_hashtag', back_populates='discussions')
    comments = relationship('Comment')

    def __repr__(self):
        return f'<Discussion {self.id}>'

    def serialise(self):
        return {"id": self.id, "author_id": self.author_id, "text": self.text, "image_url": self.image_url,
                "created_at": self.created_at, "hashtags": [hashtag.serialise() for hashtag in self.hashtags],
                "comments": [comment.serialise() for comment in self.comments], "likes_count": self.likes_count}
