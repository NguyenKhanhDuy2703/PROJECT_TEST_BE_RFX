from sqlalchemy import Column, Integer, String , Enum , TIMESTAMP , ForeignKey
import enum
from sqlalchemy.orm import relationship
from app.db.base import Base    
class statusEnum( enum.Enum):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class Task (Base) :
    __tablename__ = "tasks"
    task_id = Column (Integer, primary_key=True, index=True)
    project_id = Column (Integer, ForeignKey("projects.project_id") ,  nullable=False )
    title = Column (String, nullable=False)
    description = Column (String, nullable=True)
    status = Column (Enum(statusEnum), nullable=False , default=statusEnum.TO_DO)
    priority = Column (Integer, nullable=False , default=0)
    due_date = Column (TIMESTAMP, nullable=True)
    assignee_id = Column (Integer, nullable=True)
    create_by = Column (Integer, nullable=False)
    create_at = Column (TIMESTAMP, nullable=False)
    updated_at = Column (TIMESTAMP, nullable=True)
    project = relationship("Project", back_populates="tasks")