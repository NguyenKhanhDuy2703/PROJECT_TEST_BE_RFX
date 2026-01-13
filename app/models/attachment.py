from sqlalchemy import Column, Integer, String  , TIMESTAMP , ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base 

class Attachment (Base):
    __tablename__ = "attachments"
    attachment_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer,ForeignKey("tasks.task_id") ,  nullable=False )
    user_id = Column(Integer,  ForeignKey("users.user_id") , nullable=False )
    file_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    uploaded_at = Column(TIMESTAMP, nullable=False)
    task = relationship("Task", back_populates="attachments")
    user = relationship("User", back_populates="attachments")