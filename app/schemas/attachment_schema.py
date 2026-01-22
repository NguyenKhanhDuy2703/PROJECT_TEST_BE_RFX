from pydantic import BaseModel
from datetime import datetime
class AttachmentBase(BaseModel):
    file_name: str
    file_url: str
    file_size: int
class AttachmentCreate(AttachmentBase):
    task_id: int
    user_id: int
class AttachmentRead(AttachmentBase):
    attachment_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True