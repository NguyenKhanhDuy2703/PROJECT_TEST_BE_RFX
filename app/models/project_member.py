from sqlalchemy import Column, Integer, String  , TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base    

class Project_member (Base):
    __tablename__ = "project_members"
    project_member_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False , foreign_key="projects.project_id")
    user_id = Column(Integer, nullable=False , foreign_key="users.user_id")
    joined_at = Column(TIMESTAMP, nullable=False)
    relationship = relationship("Project", back_populates="project_members")
    relationship = relationship("User", back_populates="project_members")