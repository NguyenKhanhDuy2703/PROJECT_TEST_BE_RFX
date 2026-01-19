from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
import enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

# 1. Thêm 'str' vào để tương thích tốt với Pydantic và JSON
class StatusEnum(str, enum.Enum):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class PriorityEnum(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.TO_DO)
    priority = Column(Enum(PriorityEnum), nullable=False, default=PriorityEnum.LOW)
    due_date = Column(TIMESTAMP, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    create_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    create_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow, nullable=True)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", foreign_keys=[assignee_id])
    creator = relationship("User", foreign_keys=[create_by])
    attachments_task = relationship("Attachment", back_populates="task")
    comments_task = relationship("Comment", back_populates="task")