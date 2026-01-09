from sqlalchemy import Column, Integer, String  , TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base    

class Comment (Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=False , foreign_key="tasks.task_id")
    user_id = Column(Integer, nullable=False , foreign_key="users.user_id")
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)
    relationship = relationship("Task", back_populates="comments")
    relationship = relationship("User", back_populates="comments")