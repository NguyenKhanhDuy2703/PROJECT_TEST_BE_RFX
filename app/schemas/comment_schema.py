from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class AttachmentRead(BaseModel):
    attachment_id: int
    file_name: str
    file_url: str
    file_size: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    task_id: int

class CommentRead(CommentBase):
    comment_id: int
    task_id: int
    user_id: int       #o
    created_at: datetime
    updated_at: Optional[datetime] = None
    attachments_comment: List[AttachmentRead] = []

    class Config:
        from_attributes = True