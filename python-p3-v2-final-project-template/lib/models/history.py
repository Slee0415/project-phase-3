from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from . import Base
from datetime import datetime

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    action = Column(String)  # 'borrowed' or 'returned'
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="history")
    book = relationship("Book", back_populates="history")

    def __repr__(self):
        return f"<History(user_id={self.user_id}, book_id={self.book_id}, action={self.action}, timestamp={self.timestamp})>"
