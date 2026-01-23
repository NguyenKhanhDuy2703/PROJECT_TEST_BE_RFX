from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import verify_password , create_access_token , decode_access_token
from app.services.user_service import User_service
from fastapi import HTTPException , status
class Auth_service:
    def __init__(self  , db: AsyncSession):
        self.db = db
    async def auth_user (self , email: str , password: str) -> User:
        user_service = User_service (self.db)
        user = await user_service.get_user_by_email (email )
        if not user :
            return None
        check_password = verify_password (password , user.password_hash)
        if not check_password :
            return None
        token_data =  create_access_token (data ={"user_id": user.user_id , "email": user.email , "role" : user.role.value } )
        user.access_token = token_data
        user.token_type = "bearer"
        return user
  