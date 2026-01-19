from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import get_db
from app.services.task_service import TaskService
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task_schema import TaskCreate, TaskRead , TaskUpdate 
from app.core.auth import allow_all 
router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["tasks"],
)
def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    return TaskService(db)
@router.post("/create", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    current_user = Depends(allow_all),
    task_service: TaskService = Depends(get_task_service),
):
    try:
        new_task = await task_service.create_task(task_create, current_user)
        return new_task
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating task: {e}",
        )
@router.put("/{task_id}/update", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user = Depends(allow_all),
    task_service: TaskService = Depends(get_task_service),
):
    try:
        updated_task = await task_service.update_task(task_id, task_update, current_user)
        return updated_task
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating task: {e}",
        )
@router.get("/list", response_model=list[TaskRead], status_code=status.HTTP_200_OK)
async def list_tasks(
    project_id: int,
    status_task: str | None = None,
    assignee: int | None = None,
    priority: str | None = None,
    limit: int = 100,
    page: int = 1,
    current_user = Depends(allow_all),
    task_service: TaskService = Depends(get_task_service),
):
    try:
        tasks = await task_service.get_list_task(project_id,status_task , assignee , priority , limit , page , current_user)
        return tasks
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching tasks: {e}",
        )