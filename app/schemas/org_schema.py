from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class OrgBase(BaseModel):
    name: str
class OrgCreate(OrgBase):
    pass
class OrgRead(OrgBase):
    org_id: int
    created_at: datetime