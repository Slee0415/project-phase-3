from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    copies = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    user = relationship("User", back_populates="books")
    history = relationship("History", back_populates="book")

    def __repr__(self):
        return f"<Book(title={self.title}, author={self.author}, genre={self.genre}, copies={self.copies})>"
