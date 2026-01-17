from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Organization
from app.schemas.org_schema import OrgCreate
from datetime import datetime , timezone
class Org_service:
    def __init__(self  , db: AsyncSession):
        self.db = db
    async def create_org(self , org_create: OrgCreate) -> Organization:
        new_org = Organization(
            name=org_create.name,
            created_at = datetime.now(timezone.utc).replace(tzinfo=None)
        )
        self.db.add(new_org)
        await self.db.commit()
        await self.db.refresh(new_org)
        return new_org  