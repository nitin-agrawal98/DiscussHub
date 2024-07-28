from sqlalchemy import Column, BIGINT, String, INTEGER
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BIGINT, primary_key=True)
    name = Column(String(200), nullable=False)
    mobile = Column(String(13), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(500), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialise(self):
        return {"id": self.id, "name": self.name, "mobile": self.mobile, "email": self.email}
