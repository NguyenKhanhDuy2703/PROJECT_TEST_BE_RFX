from fastapi import Depends , HTTPException, status ,APIRouter, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.attachment_service import AttachmentService
from app.db.session import get_db
from app.schemas.attachment_schema import AttachmentRead
from app.core.auth import allow_all
from typing import List
router = APIRouter(
    prefix="/api/v1/attachments",
    tags=["attachments"],
)
def get_attachment_service(db: AsyncSession = Depends(get_db)) -> AttachmentService:
    return AttachmentService(db)
@router.post("/upload", response_model=AttachmentRead, status_code=status.HTTP_201_CREATED)
async def upload_attachment(
    task_id: int = Form(...),
    file: UploadFile = File(...),
    current_user = Depends(allow_all),
    attachment_service: AttachmentService = Depends(get_attachment_service),
):
    try:
        new_attachment = await attachment_service.upload_attachment(task_id, file, current_user)
        return new_attachment
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error uploading attachment: {e}",
        )
