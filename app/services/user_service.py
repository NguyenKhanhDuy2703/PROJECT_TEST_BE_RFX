from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.organization import Organization
from app.schemas.user_schema import UserCreate
from app.schemas.org_schema import OrgRead
from datetime import datetime
from sqlalchemy import select 
from datetime import timezone
from app.core.security import get_password_hash , verify_password
class User_service:
    def __init__(self  , db: AsyncSession):
        self.db = db
    async def create_user(self , user_create: UserCreate ) -> User:
        print (user_create)
        check_user = await self.db.execute(select (User).where (User.email == user_create.email) ) 
        if check_user.scalars().first() :
            raise Exception ("Email already exists " )
        check_org = await self.db.execute(select (Organization).where (Organization.org_id == user_create.org_id) )
        org = check_org.scalars().first()
        if not org :
            raise Exception ("Organization does not exist " )
        hashed_password = get_password_hash (user_create.password)
        new_user = User(
            org_id = user_create.org_id,
            email=user_create.email,
            password_hash=hashed_password, 
            full_name=user_create.full_name,
            role=user_create.role.upper(),
            created_at = datetime.now(timezone.utc).replace(tzinfo=None)
            )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    async def get_user_by_email (self , email: str ) -> User:
        check_user = await self.db.execute(select (User).where (User.email == email) ) 
        user = check_user.scalars().first()
        if not user :
            raise Exception ("user does not exist " )
        return user
    
         
