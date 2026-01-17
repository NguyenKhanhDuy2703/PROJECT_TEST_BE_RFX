from fastapi import APIRouter , Depends , HTTPException , status
from app.db.session import get_db
from app.schemas.org_schema import OrgCreate
from app.services.org_service import Org_service
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter(
    prefix="/api/v1/orgs",
    tags=["organizations"],
)
def get_user_service(db : AsyncSession =Depends(get_db) ) -> Org_service :
    return Org_service (db)

@router.post("/create" , status_code=status.HTTP_200_OK )
async def create_org(
    org_create: OrgCreate ,
    org_service: Org_service = Depends(get_user_service),
):
    try:
        new_org = await org_service.create_org(org_create )
        return {"message": "Organization created successfully", "org_id": new_org}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating organization: {e}",
        )
    