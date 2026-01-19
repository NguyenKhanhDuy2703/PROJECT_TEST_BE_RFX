from fastapi import APIRouter , Depends , HTTPException , status
from app.db.session import get_db
from app.services.project_service import ProjectService
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.project_schema import ProjectCreate , ProjectMemberRead ,ProjectMemberCreate , ProjectMemberDelete
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

@router.post("/{project_id}/add-member" , response_model= ProjectMemberRead , status_code=status.HTTP_200_OK )
async def add_member_to_project (
    project_id : int ,
    member_data  : ProjectMemberCreate,
    current_user = Depends(allow_manager_admin) ,
    project_service : ProjectService = Depends ( get_project_service )
):
    try :
        new_member = await project_service.add_user_to_project ( project_id , member_data , current_user )
        return new_member
    except HTTPException as http_exc :
        raise http_exc
    except Exception as e :
        raise HTTPException (
            status_code = status.HTTP_400_BAD_REQUEST ,
            detail = f" Error adding member to project : { e } "
        )
@router.post("/{project_id}/delete-member"  , status_code=status.HTTP_200_OK )
async def delete_member_from_project (
    project_id : int ,
    member_data  : ProjectMemberDelete,
    current_user = Depends(allow_manager_admin) ,
    project_service : ProjectService = Depends ( get_project_service )
):
 
    try :
        deleted_member = await project_service.delete_user_from_project ( project_id , member_data.email , current_user )
        return deleted_member
    except HTTPException as http_exc :
        raise http_exc
    except Exception as e :
        raise HTTPException (
            status_code = status.HTTP_400_BAD_REQUEST ,
            detail = f" Error deleting member from project : { e } "
        )