from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from sqlalchemy import select
from app.core.security import verify_password , create_access_token , decode_access_token
from app.services.user_service import User_service
class Auth_service:
    def __init__(self  , db: AsyncSession):
        self.db = db
    async def auth_user (self , email: str , password: str) -> User:
        user = await User_service.get_user_by_email (self , email )
        check_password = verify_password (password , user.password_hash)
        if not check_password :
            raise Exception ("Incorrect password " )
        token_data =  create_access_token (data ={"user_id": user.user_id , "email": user.email , "role" : user.role.value } )
        user.access_token = token_data
        user.token_type = "bearer"
        return user
    async def verify_token (self , token: str ) -> dict :
        try :
            payload =  decode_access_token (token )
            if not payload :
                raise Exception ("Invalid token " )
            user_id = payload.get ("user_id" )
            if not user_id :
                raise Exception("Token payload missing user info")
            query = await self.db.execute (select (User).where (User.user_id == user_id ) )
            user = query.scalars().first()
            if not user :
                raise Exception ("User not found " )
            
            return user
        except Exception as e:
            print(f"DEBUG ERROR verify_token: {e}")
            raise e