from fastapi import APIRouter , Depends , HTTPException , status
from app.db.session import get_db
from app.schemas.user_schema import UserCreate, UserRead , UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import User_service
from app.services.auth_service import Auth_service
router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)

def get_user_service(db : AsyncSession =Depends(get_db) ) -> User_service :
    return User_service (db)

@router.post("/signup" , response_model=UserRead , status_code=status.HTTP_201_CREATED)
async def signup(
    user_create: UserCreate, # kiểu dữ liệu đầu vào phải mapping với usercreate schema
    user_service: User_service = Depends(get_user_service), # lấy hàm xử ly service
):
    try:
        new_user = await user_service.create_user(user_create)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {e}",
        )
def get_auth_service(db : AsyncSession =Depends(get_db) ) -> Auth_service :
    return Auth_service (db)

@router.get("/signin" , response_model=UserRead )
async def sigin(
    user_login: UserLogin,  
    auth_service: Auth_service = Depends(get_auth_service),
):
    print (user_login)
    try:
        user = await auth_service.auth_user (user_login.email , user_login.password )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error logging in user: {e}",
        )