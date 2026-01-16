from sqlalchemy import Column, Integer, String  , TIMESTAMP , ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base    

class Comment (Base):
    __tablename__ = "comments"
    comment_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer,ForeignKey("tasks.task_id") , nullable=False )
    user_id = Column(Integer,ForeignKey("users.user_id"), nullable=False )
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)
    task = relationship("Task", back_populates="comments_task")
    user = relationship("User", back_populates="comments_user")