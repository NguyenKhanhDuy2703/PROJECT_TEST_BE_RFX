from sqlalchemy import Column, Integer, String , TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base   
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, nullable=False , foreign_key="organizations.org_id")
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    relationship = relationship("Organization", back_populates="users")