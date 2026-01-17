from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserRead, UserLogin , TokenData
from app.services.user_service import User_service
from app.services.auth_service import Auth_service
from app.core.auth import allow_admin
router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


def get_user_service(db: AsyncSession = Depends(get_db)) -> User_service:
    return User_service(db)

def get_auth_service(db: AsyncSession = Depends(get_db)) -> Auth_service:
    return Auth_service(db)


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_200_OK)
async def signup(
    user_create: UserCreate,
    check_role = Depends(allow_admin),
    user_service: User_service = Depends(get_user_service),
):
    try:
        new_user = await user_service.create_user(user_create)
        return new_user
    except Exception as e:
        print (e)
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


