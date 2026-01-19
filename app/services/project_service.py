from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import Project
from app.schemas.project_schema import  ProjectMemberCreate
from app.models.organization import Organization
from app.models.user import User
from app.models.project_member import Project_member
from sqlalchemy import select
from datetime import datetime , timezone
from fastapi import HTTPException , status
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
    

    async def add_user_to_project( self ,project_id : int , member , current_user : User ):
    
        result  = await self.db.execute (select(Project).where (Project.project_id == project_id  , Project.org_id == current_user.org_id ) )
        project = result.scalars().first()
        if not project :
            raise HTTPException(status_code=404 , detail = "Project not found  or access denied" )
        get_member = await self.db.execute ( select (User).where ( User.email == member.email  , User.org_id == current_user.org_id ) )
        user = get_member.scalars().first()
        if not user :
            raise HTTPException ( status_code =404 , detail = "User not found in your organization " )
        add_new_member = Project_member (
            project_id = project.project_id ,
            user_id = user.user_id ,
            joined_at = datetime.now ( timezone.utc ).replace( tzinfo = None )
        )
        self.db.add ( add_new_member )
        await self.db.commit()
        await self.db.refresh ( add_new_member )
        return add_new_member
        
    async def delete_user_from_project ( self , project_id : int , email : int , current_user : User ):
        result  = await self.db.execute (select(Project).where (Project.project_id == project_id  , Project.org_id == current_user.org_id ) )
        project = result.scalars().first()
        if not project :
            raise HTTPException(status_code=404 , detail = "Project not found  or access denied" )
        user = await self.db.execute(select (User).where (User.email == email  , User.org_id == current_user.org_id ) )
        user = user.scalars().first()
    
        if not user :
            raise HTTPException ( status_code =404 , detail = "User not found in your organization " )
        print ( f" Deleting user { user.user_id } from project { project_id } " )
        get_member = await self.db.execute ( select (Project_member).where ( Project_member.user_id == user.user_id  , Project_member.project_id == project_id ) )
        member = get_member.scalars().first()

        if not member :
            raise HTTPException ( status_code =404 , detail = "User not a member of this project " )
        await self.db.delete ( member )
        await self.db.commit()
        return True

