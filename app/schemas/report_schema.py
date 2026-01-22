from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.schemas.task_schema import TaskRead 

class TaskStats(BaseModel):
    TO_DO: int = 0
    IN_PROGRESS: int = 0
    COMPLETED: int = 0

class ProjectReportResponse(BaseModel):
    project_id: int
    generated_at: datetime
    stats: TaskStats 
    overdue_tasks: List[TaskRead] 

    class Config:
        from_attributes = True