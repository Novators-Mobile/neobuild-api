from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

from app.database.session import Base


class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=True)
    author = Column(String, nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    release_id = Column(Integer, ForeignKey("releases.id"), nullable=True)
    branch_name = Column(String, nullable=True)
    in_release = Column(Boolean, default=False)
    committed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    task = relationship("Task", back_populates="commits")
    release = relationship("Release", back_populates="commits") 