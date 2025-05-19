from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import datetime
import enum

from app.database.session import Base


class MergeRequestStatus(enum.Enum):
    OPEN = "open"
    MERGED = "merged"
    CLOSED = "closed"
    CONFLICT = "conflict"


class MergeRequest(Base):
    __tablename__ = "merge_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    source_branch = Column(String, nullable=False)
    target_branch = Column(String, nullable=False)
    status = Column(Enum(MergeRequestStatus), default=MergeRequestStatus.OPEN)
    can_be_merged = Column(Boolean, default=False)
    assigned_to = Column(String, nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    release_id = Column(Integer, ForeignKey("releases.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    task = relationship("Task")
    release = relationship("Release", back_populates="merge_requests") 