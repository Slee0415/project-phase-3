from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)

    books = relationship("Book", back_populates="user")
    history = relationship("History", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username})>"
