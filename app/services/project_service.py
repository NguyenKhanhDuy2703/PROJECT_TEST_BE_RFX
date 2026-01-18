from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import Project
from app.schemas.project_schema import ProjectCreate
from app.models.organization import Organization
from sqlalchemy import select
from datetime import datetime , timezone
class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create_project(self , project_data):
        
        check_org = await self.db.execute(select (Organization).where (Organization.org_id == project_data.org_id) )
        org = check_org.scalars().first()
        if not org :
            raise Exception ("Organization does not exist " )
        new_project = Project(
            org_id=project_data.org_id,
            name=project_data.name,
            description=project_data.description,
            created_at = datetime.now(timezone.utc).replace(tzinfo=None)
        )
        self.db.add(new_project)
        await self.db.commit()
        await self.db.refresh(new_project)
        return new_project
    async def list_projects(self , org_id: int = None):
        check_org = await self.db.execute(select (Organization).where (Organization.org_id == org_id) )
        org = check_org.scalars().first()
        if not org :
            raise Exception ("Organization does not exist " )
        result = await self.db.execute(select (Project).where (Project.org_id == org_id) )
        projects = result.scalars().all()
        return projects
        

