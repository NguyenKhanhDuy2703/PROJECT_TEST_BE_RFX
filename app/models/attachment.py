from sqlalchemy import Column, Integer, String  , TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base 

class Attachment (Base):
    __tablename__ = "attachments"
    attachment_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=False , foreign_key="tasks.task_id")
    user_id = Column(Integer, nullable=False , foreign_key="users.user_id")
    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    uploaded_at = Column(TIMESTAMP, nullable=False)
    relationship = relationship("Task", back_populates="attachments")
    relationship = relationship("User", back_populates="attachments")