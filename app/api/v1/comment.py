from fastapi import HTTPException, status ,APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.comment_service import CommentService
from app.db.session import get_db
from app.schemas.comment_schema import CommentCreate , CommentRead
from app.core.auth import allow_all
router = APIRouter(
    prefix="/api/v1/comments",
    tags=["comments"],
)
def get_task_service(db: AsyncSession = Depends(get_db)) -> CommentService:
    return CommentService(db)
@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    current_user = Depends(allow_all),
    comment_service: CommentService = Depends(get_task_service),
):
    try:
        new_comment = await comment_service.create_comment(comment_data , current_user)
        return new_comment
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating comment: {e}",
        )