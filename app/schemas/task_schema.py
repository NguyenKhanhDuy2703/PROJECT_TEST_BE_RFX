from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class PriorityEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskStatus(str, Enum):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TO_DO 
    priority: PriorityEnum = PriorityEnum.MEDIUM

class TaskCreate(TaskBase):
    project_id: int
    assignee_id: Optional[int] = None 
    due_date: Optional[datetime] = None
    priority: PriorityEnum 

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None     
    priority: Optional[PriorityEnum] = None 
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None       

class TaskRead(TaskBase):
    task_id: int
    project_id: int
    assignee_id: Optional[int] = None
    create_by: int 
    due_date: Optional[datetime] = None 
    create_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True