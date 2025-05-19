from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

from app.database.session import Base


class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    is_release_branch = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="branches")
    release = relationship("Release", back_populates="branch", uselist=False)
    tasks = relationship("Task", back_populates="branch") 