from sqlalchemy import Column, BIGINT, DATETIME, TEXT, String, ForeignKey
from sqlalchemy.orm import relationship

from utils.time import get_current_time
from .base import Base


class Hashtag(Base):
    __tablename__ = 'hashtag'

    id = Column(BIGINT, primary_key=True)
    author_id = Column(BIGINT, nullable=False)
    tag = Column(String(10), unique=True)
    created_at = Column(DATETIME, default=get_current_time)

    discussions = relationship('Discussion', secondary='discussion_hashtag', back_populates='hashtags')

    def __repr__(self):
        return f'<HashTag {self.id}>'

    def serialise(self):
        return {"id": self.id, "tag": self.tag, "author_id": self.author_id}
