from fastapi import APIRouter , Depends , HTTPException , status
from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserRead