from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timezone

from app.models.task import Task, StatusEnum
from app.models.project_member import Project_member
from app.models.project import Project  
from app.models.user import User, RoleEnum 

class ReportService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_task_report(self, project_id: int, current_user: User):
        query_project = select(Project).where(Project.project_id == project_id)
        project = (await self.db.execute(query_project)).scalars().first()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Project not found"
            )

        query_member = select(Project_member).where(
            Project_member.project_id == project_id,
            Project_member.user_id == current_user.user_id
        )
        is_member = (await self.db.execute(query_member)).scalars().first()
        if not is_member and current_user.role != RoleEnum.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Access denied"
            )
        query_stats = (
            select(Task.status, func.count(Task.task_id))
            .where(Task.project_id == project_id)
            .group_by(Task.status)
        )
        result_stats = await self.db.execute(query_stats)
        stats_map = {row[0].value: row[1] for row in result_stats.all()}

        now = datetime.now(timezone.utc).replace(tzinfo=None)
        
        query_overdue_list = (
            select(Task) 
            .where(
                Task.project_id == project_id,
                Task.due_date < now,
                Task.status != StatusEnum.COMPLETED 
            )
            .order_by(Task.due_date.asc()) 
        )
        
        result_overdue = await self.db.execute(query_overdue_list)
        overdue_tasks = result_overdue.scalars().all() 

        return {
            "project_id": project_id,
            "generated_at": datetime.now(),
            "stats": {
                "TO_DO": stats_map.get("TO_DO", 0),
                "IN_PROGRESS": stats_map.get("IN_PROGRESS", 0),
                "DONE": stats_map.get("DONE", 0) 
            },
            "overdue_tasks": overdue_tasks 
        }