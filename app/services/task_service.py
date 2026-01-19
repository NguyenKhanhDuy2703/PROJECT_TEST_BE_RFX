from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.task import Task , StatusEnum
from app.models.project_member import Project_member
from app.models.user import User, RoleEnum
from app.schemas.task_schema import TaskCreate , TaskUpdate


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_membership(self, project_id: int, user_id: int):
        result = await self.db.execute(
            select(Project_member).where(
                Project_member.project_id == project_id,
                Project_member.user_id == user_id
            )
        )
        member = result.scalars().first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Access denied: You are not a member of this project"
            )
        return member

    async def check_due_date (self , due_date : datetime ):
        now = datetime.now()
        if due_date < now :
            raise HTTPException (
                status_code = status.HTTP_400_BAD_REQUEST ,
                detail = " Due date must be in the future " 
            )
        
    async def create_task(self, task_data: TaskCreate, current_user: User):
        await self._check_membership(task_data.project_id, current_user.user_id)

        if task_data.due_date:
            await self.check_due_date(task_data.due_date)
            
        assignee_id = current_user.user_id 
        
        if current_user.role == RoleEnum.MEMBER:
            if assignee_id and assignee_id != current_user.user_id:
                raise HTTPException(status_code=403, detail="Members can only assign tasks to themselves")

        elif assignee_id:
             assignee_id = task_data.assigned_to
             await self._check_membership(task_data.project_id, assignee_id)


        new_task = Task(
            project_id=task_data.project_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            status=StatusEnum.TO_DO,
            due_date=task_data.due_date,
            assignee_id=assignee_id,
            create_by=current_user.user_id,
            create_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return new_task
    
    async def update_task(self, task_id: int, task_update: TaskUpdate, current_user: User):
    
        query = select(Task).where(Task.task_id == task_id)
        result = await self.db.execute(query)
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        await self._check_membership(task.project_id, current_user.user_id)

        update_data = task_update.model_dump(exclude_unset=True)

        if "status" in update_data:
            new_status = update_data["status"]
            current_status = task.status
    
            valid_transition = False
            if current_status == StatusEnum.TO_DO and new_status == StatusEnum.IN_PROGRESS:
                valid_transition = True
            elif current_status == StatusEnum.IN_PROGRESS and new_status == StatusEnum.COMPLETED:
                valid_transition = True    
            elif current_status == new_status:
                valid_transition = True

            if not valid_transition:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid status transition from {current_status} to {new_status}"
                )

        for key, value in update_data.items():
            setattr(task, key, value)
        
        task.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        
        await self.db.commit()
        await self.db.refresh(task)
        return task

    
    async def get_list_task(self, project_id: int , status_task : str | None , assignee : int | None , priority : str | None  , limit : int  , page : int ,  current_user: User ):
        query = select(Task).where(Task.project_id == project_id)
        await self._check_membership(project_id, current_user.user_id)
        if status_task :
            query = query.where ( Task.status == StatusEnum ( status_task ) )
        if assignee :
            query = query.where ( Task.assignee_id == assignee )
        if priority :
            query = query.where ( Task.priority == priority  )
        query = query.limit ( limit ).offset ( ( page -1 ) * limit  )
        result = await self.db.execute ( query )
        tasks = result.scalars().all()
        return tasks
    

       
            