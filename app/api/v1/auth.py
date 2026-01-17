from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserRead, UserLogin , TokenData
# Giả sử bạn có schema Token trả về
from pydantic import BaseModel 

from app.services.user_service import User_service
from app.services.auth_service import Auth_service
from app.models.user import User

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/signin")


def get_user_service(db: AsyncSession = Depends(get_db)) -> User_service:
    return User_service(db)

def get_auth_service(db: AsyncSession = Depends(get_db)) -> Auth_service:
    return Auth_service(db)

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    auth_service: Auth_service = Depends(get_auth_service)
) -> User:
    try:
        user = await auth_service.verify_token(token)
        if not user:
             raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_200_OK)
async def signup(
    user_create: UserCreate,
    user_service: User_service = Depends(get_user_service),
):
    try:
        new_user = await user_service.create_user(user_create)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {e}",
        )

@router.post("/signin", response_model=TokenData , status_code=status.HTTP_200_OK) 
async def signin(
    user_login: UserLogin,  
    auth_service: Auth_service = Depends(get_auth_service),
):
    user = await auth_service.auth_user(user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = await  auth_service.auth_user(user_login.email, user_login.password)

    return access_token

@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: User = Depends(get_current_user) 
):
    return current_user