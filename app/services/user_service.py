from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, RoleEnum
from app.models.organization import Organization
from app.schemas.user_schema import UserCreate
from datetime import datetime, timezone
from sqlalchemy import select 
from app.core.security import get_password_hash
import logging

logger = logging.getLogger(__name__)

class User_service:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_create: UserCreate, current_user_org_id: int = None) -> User:
        logger.info(f"Creating user: {user_create.email}")
   
        check_user = await self.db.execute(select(User).where(User.email == user_create.email)) 
        if check_user.scalars().first():
            raise Exception("Email already exists")
        org_id_to_use = current_user_org_id if current_user_org_id else user_create.org_id

        check_org = await self.db.execute(select(Organization).where(Organization.org_id == org_id_to_use))
        org = check_org.scalars().first()
        if not org:
            raise Exception("Organization does not exist")
        hashed_password = get_password_hash(user_create.password)
        try:
            role_enum = RoleEnum(user_create.role.lower()) 
        except ValueError:
            role_enum = RoleEnum.MEMBER 

        new_user = User(
            org_id=org_id_to_use,
            email=user_create.email,
            password_hash=hashed_password, 
            full_name=user_create.full_name,
            role=role_enum,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )
        
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def get_user_by_email(self, email: str) -> User:
        result = await self.db.execute(select(User).where(User.email == email)) 
        user = result.scalars().first()
        return user