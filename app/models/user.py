from sqlalchemy import Column, Integer, String , TIMESTAMP , Enum , ForeignKey
import enum
from sqlalchemy.orm import relationship
from app.db.base import Base   
class RoleEnum(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer,  ForeignKey("organizations.org_id") , nullable=False )
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False , default=RoleEnum.MEMBER)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    organization = relationship("Organization", back_populates="users" )
    project_members = relationship("Project_member", back_populates="user")
    attachments_user = relationship("Attachment", back_populates="user")
    comments_user = relationship("Comment", back_populates="user")
    notifications = relationship("Notification", back_populates="recipient")