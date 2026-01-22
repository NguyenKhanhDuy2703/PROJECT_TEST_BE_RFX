from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    task_id: int

class CommentRead(CommentBase):
    comment_id: int
    task_id: int
    user_id: int       
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True