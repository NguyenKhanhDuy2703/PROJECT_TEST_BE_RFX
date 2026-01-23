from  fastapi import Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user_schema import TokenData
from app.models.user import User , RoleEnum
from app.core.security import  decode_access_token
from sqlalchemy import select
from typing import List
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/signin")
async def authenticate_user (token : str = Depends(oauth2_scheme) , db: AsyncSession = Depends(get_db)) -> TokenData:
    
    try:
        payload = decode_access_token (token )
        print (payload)
        if not payload :
            raise "Invalid token "
        check_user_id = await db.execute (select (User).where (User.user_id == payload.get("user_id") ) )
        user = check_user_id.scalars().first()
        if not user :
           return None
        return user
    except Exception as e:
        raise HTTPException (
            status_code = status.HTTP_401_UNAUTHORIZED ,
            detail =f"Could not validate credentials : {e } " ,
            headers ={"WWW-Authenticate" : "Bearer" }
        )
    
class Authoticate_user :
    def __init__(self  , allow_roles: List [RoleEnum] =[] ):
       self.allow_roles = allow_roles
    def __call__(self, user = Depends(authenticate_user)) -> User:
        if user.role not in self.allow_roles :
            raise HTTPException (
                status_code = status.HTTP_403_FORBIDDEN ,
                detail = "You do not have permission to access this resource " 
            )
        return user

allow_admin = Authoticate_user (allow_roles =[ RoleEnum.ADMIN ] )
allow_manager_admin = Authoticate_user (allow_roles =[ RoleEnum.MANAGER , RoleEnum.ADMIN ] )
allow_all = Authoticate_user (allow_roles =[ RoleEnum.MEMBER , RoleEnum.MANAGER , RoleEnum.ADMIN ] )