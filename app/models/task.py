from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
import datetime
import enum

from app.database.session import Base


class TaskStatus(enum.Enum):
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    FOR_RELEASE = "For Release"
    IN_RELEASE = "In Release"
    DONE = "Done"


# Task dependencies association table
task_dependencies = Table(
    "task_dependencies",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("dependency_id", Integer, ForeignKey("tasks.id"), primary_key=True)
)

# Task tags association table
task_tags = Table(
    "task_tags",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default=TaskStatus.TO_DO.value)
    author = Column(String, nullable=True)
    developer = Column(String, nullable=True)
    is_release_task = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True)
    release_id = Column(Integer, ForeignKey("releases.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    branch = relationship("Branch", back_populates="tasks")
    release = relationship("Release", back_populates="tasks")
    commits = relationship("Commit", back_populates="task")
    
    # Task dependencies (many-to-many self-referential)
    dependencies = relationship(
        "Task",
        secondary=task_dependencies,
        primaryjoin=id==task_dependencies.c.task_id,
        secondaryjoin=id==task_dependencies.c.dependency_id,
        backref="dependent_tasks"
    )
    
    # Task tags (many-to-many)
    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")


class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False, unique=True)
    
    # Relationships
    tasks = relationship("Task", secondary=task_tags, back_populates="tags") 