from pydantic import BaseModel
from datetime import datetime
class ProjectBase(BaseModel):
    name : str 
    description : str
class ProjectCreate(ProjectBase):
    org_id : int
class ProjectRead(ProjectBase):
    project_id : int
    org_id : int
    created_at : datetime
