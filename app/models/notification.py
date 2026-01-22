from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Enum
import enum
from datetime import datetime
from sqlalchemy.orm import relationship
from app.db.base import Base

class NotificationTypeEnum(str, enum.Enum):
    TASK_ASSIGNED = "TASK_ASSIGNED"  
    TASK_STATUS_CHANGED = "TASK_STATUS_CHANGED" 
    COMMENT_ADDED = "COMMENT_ADDED"      

class Notification(Base):
    __tablename__ = "notifications"
    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False) 
    task_id = Column(Integer, ForeignKey("tasks.task_id"), nullable=True)  
    content = Column(String, nullable=False)
    type = Column(Enum(NotificationTypeEnum), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    recipient = relationship("User", back_populates="notifications")