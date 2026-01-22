from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Union
from app.models.notification import NotificationTypeEnum

class NotificationBase(BaseModel):
    content: str
    type: NotificationTypeEnum
    task_id: Optional[int] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationRead(NotificationBase):
    notification_id: int
    user_id: int
    is_read: bool
    created_at: Union[datetime, str] 

    class Config:
        from_attributes = True