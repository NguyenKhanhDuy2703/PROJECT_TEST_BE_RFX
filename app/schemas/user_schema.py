from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str 
    org_id: int
    role: str

class UserRead(UserBase):
    user_id: int
    role: str
    full_name: Optional[str] = None
    password: Optional[str] = None
    
class UserResponse(UserBase):
    user_id: int
    created_at: datetime
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    access_token: str
    token_type: str