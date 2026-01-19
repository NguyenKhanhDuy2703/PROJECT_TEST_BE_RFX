from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    name: str 
    description: str

class ProjectCreate(ProjectBase):
    org_id: int

class ProjectRead(ProjectBase):
    project_id: int
    org_id: int
    created_at: datetime

class ProjectMemberCreate(BaseModel):
    email: EmailStr
    role: Optional[str] = "member"

class ProjectMemberRead(BaseModel):
    project_id: int
    user_id: int
    joined_at: Optional[datetime] = None

    class Config:
        from_attributes = True 
class ProjectMemberDelete(BaseModel):
    email: EmailStr