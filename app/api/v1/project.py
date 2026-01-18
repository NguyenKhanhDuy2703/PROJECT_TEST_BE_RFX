from fastapi import APIRouter , Depends , HTTPException , status
from app.db.session import get_db
from app.services.project_service import ProjectService
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.project_schema import ProjectCreate , ProjectRead
from app.core.auth import allow_manager_admin , allow_all
router = APIRouter(
    prefix="/api/v1/projects",
    tags=["projects"],
)
def get_project_service(db : AsyncSession = Depends(get_db) ) -> ProjectService :
    return ProjectService (db)
@router.post("/create" , status_code=status.HTTP_200_OK )
async def create_project(
    project_create: ProjectCreate ,
    check_role = Depends(allow_manager_admin),
    project_service: ProjectService = Depends(get_project_service),
):
    try:
        new_project = await project_service.create_project(project_create )
        return {"message": "Project created successfully", "project_id": new_project.project_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating project: {e}",
        )
@router.get("/list" , status_code=status.HTTP_200_OK)
async def list_projects(
    org_id: int ,
    check_role = Depends(allow_all),
    project_service: ProjectService = Depends(get_project_service),
):
    try:
        
        projects = await project_service.list_projects(org_id)
        return projects
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching projects: {e}",
        )

    