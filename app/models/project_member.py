from sqlalchemy import Column, Integer, String  , TIMESTAMP , ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base    

class Project_member (Base):
    __tablename__ = "project_members"
    project_member_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id") , nullable=False )
    user_id = Column(Integer,ForeignKey("users.user_id") , nullable=False )
    joined_at = Column(TIMESTAMP, nullable=False)
    project = relationship("Project", back_populates="project_members")
    user = relationship("User", back_populates="project_members")