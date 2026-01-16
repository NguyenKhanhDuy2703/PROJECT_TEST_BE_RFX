from sqlalchemy import Column, Integer, String , TIMESTAMP , ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base    

class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer,ForeignKey("organizations.org_id"), nullable=False )
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    organization = relationship("Organization", back_populates="projects")
    project_members = relationship("Project_member", back_populates="project")
    tasks = relationship("Task", back_populates="project")