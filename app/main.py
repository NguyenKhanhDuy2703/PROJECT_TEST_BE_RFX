from fastapi import FastAPI

from app.api.v1 import auth
from app.api.v1 import org
from app.api.v1 import project
from app.api.v1 import task
from app.api.v1 import comment

from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException , Depends , status , APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
import app.models 
from app.core.logging import setup_logging
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler
)
setup_logging()


app = FastAPI(title="My FastAPI Application")

app.include_router(auth.router)
app.include_router(org.router)
app.include_router(project.router)
app.include_router(task.router)
app.include_router(comment.router)

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

router = APIRouter(
    prefix="/api/v1",
    tags=["health"],
)
@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        # Kiểm tra kết nối Database có ổn không
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "details": str(e)}
app.include_router(router)