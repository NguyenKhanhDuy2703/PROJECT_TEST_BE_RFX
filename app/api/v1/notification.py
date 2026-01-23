from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.notification_service import NotificationService
from app.schemas.notification_schema import NotificationRead
from app.core.auth import allow_all 

router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["notifications"],
)

@router.get("/", response_model=list[NotificationRead])
async def get_notifications(
    limit: int = 20,
    offset: int = 0,
    current_user = Depends(allow_all), 
    db: AsyncSession = Depends(get_db)
):
    service = NotificationService(db)
    notifications = await service.get_my_notifications( current_user, limit=limit, offset=offset)
    return notifications