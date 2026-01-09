from sqlalchemy import Column, Integer, String , TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base    

class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, nullable=False , foreign_key="organizations.org_id")
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    relationship = relationship("Organization", back_populates="projects")