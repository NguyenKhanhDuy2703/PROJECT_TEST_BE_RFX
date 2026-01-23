from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.notification import Notification, NotificationTypeEnum
from app.models.task import Task
from app.models.user import User
from app.core.redis import redis_client
import json
from datetime import datetime

class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create_notification(self, user_id: int, content: str, type: NotificationTypeEnum, task_id: int = None):
        new_notification = Notification(
            user_id=user_id,
            content=content,
            type=type,
            task_id=task_id,
            created_at=datetime.utcnow()
        )
        self.db.add(new_notification)
        
        redis_key = f"user:{user_id}:notifications"
        notification_data = {
            "notification_id": "temp",
            "user_id": user_id,
            "content": content,
            "type": type,
            "task_id": task_id,
            "is_read": False,
            "created_at": str(datetime.utcnow())
        }
        await redis_client.lpush(redis_key, json.dumps(notification_data))
        await redis_client.ltrim(redis_key, 0, 19)

        return new_notification

  
    async def notify_task_assigned(self, task: Task, assigner: User):
        if task.assignee_id and task.assignee_id != assigner.user_id:
            content = f"You have been assigned to task '{task.title}' by {assigner.full_name}"
            await self.create_notification(
                user_id=task.assignee_id,
                content=content,
                type=NotificationTypeEnum.TASK_ASSIGNED,
                task_id=task.task_id
            )

    async def notify_task_status_changed(self, task: Task, modifier: User, old_status: str):
        if task.assignee_id and task.assignee_id != modifier.user_id:
             content = f"Task '{task.title}' status changed from {old_status} to {task.status}"
             await self.create_notification(
                user_id=task.assignee_id,
                content=content,
                type=NotificationTypeEnum.TASK_STATUS_CHANGED,
                task_id=task.task_id
            )
             
    async def get_my_notifications(self, current_user: User , limit: int = 20, offset: int = 0):
        result = await self.db.execute(select(Notification).where(Notification.user_id == current_user.user_id).order_by(Notification.created_at.desc()).offset(offset).limit(limit))
        notifications = result.scalars().all()
        return notifications
    
    async def mark_notification_as_read(self, notification_id: int, current_user: User):
        query = select(Notification).where(Notification.notification_id == notification_id, Notification.user_id == current_user.user_id)
        result = await self.db.execute(query)
        notification = result.scalars().first()
        if not notification:
            return None
        notification.is_read = True
        await self.db.commit()
        await self.db.refresh(notification)
        return notification