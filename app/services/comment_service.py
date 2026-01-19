from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from datetime import datetime

from app.models.comment import Comment
from app.models.task import Task         
from app.models.project_member import Project_member
from app.schemas.comment_schema import CommentCreate 
from app.models.user import User

class CommentService:
    def __init__(self, db: AsyncSession):   
        self.db = db

    async def create_comment(self, comment_data: CommentCreate, current_user: User) -> Comment:
        query_task = select(Task).where(Task.task_id == comment_data.task_id)
        result_task = await self.db.execute(query_task)
        task = result_task.scalars().first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task does not exist")
        project_id = task.project_id
        
        query_member = select(Project_member).where(
            Project_member.project_id == project_id,
            Project_member.user_id == current_user.user_id
        )
        member_check = await self.db.execute(query_member)
        if not member_check.scalars().first():
             raise HTTPException(status_code=403, detail="Access denied: You are not a member of this project")
        new_comment = Comment(
            task_id=comment_data.task_id,
            content=comment_data.content,
            user_id=current_user.user_id,
            created_at=datetime.utcnow() 
        )

        self.db.add(new_comment)
        await self.db.commit()
        await self.db.refresh(new_comment)
        
        return new_comment