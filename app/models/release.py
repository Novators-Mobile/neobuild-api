from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import datetime
import enum

from app.database.session import Base


class ReleaseStatus(enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(ReleaseStatus), default=ReleaseStatus.DRAFT)
    project_id = Column(Integer, ForeignKey("projects.id"))
    branch_id = Column(Integer, ForeignKey("branches.id"))
    skip_pipeline = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="releases")
    branch = relationship("Branch", foreign_keys=[branch_id], back_populates="release")
    tasks = relationship("Task", foreign_keys="[Task.release_id]", back_populates="release")
    merge_requests = relationship("MergeRequest", back_populates="release")
    checks = relationship("ReleaseCheck", back_populates="release")
    commits = relationship("Commit", back_populates="release")


class ReleaseCheck(Base):
    __tablename__ = "release_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    release_id = Column(Integer, ForeignKey("releases.id"))
    check_type = Column(String, nullable=False)  # task_status, task_dependencies, project_dependencies, commit_check
    status = Column(String, nullable=False)  # success, warning, error
    message = Column(Text, nullable=True)
    details = Column(Text, nullable=True)  # JSON serialized data
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    release = relationship("Release", back_populates="checks") 