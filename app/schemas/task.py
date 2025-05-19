from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagInDB(TagBase):
    id: int
    
    class Config:
        orm_mode = True


class Tag(TagInDB):
    pass


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    author: Optional[str] = None
    developer: Optional[str] = None
    is_release_task: bool = False
    project_id: int
    branch_id: Optional[int] = None
    release_id: Optional[int] = None


class TaskCreate(TaskBase):
    tags: Optional[List[str]] = None
    dependency_ids: Optional[List[int]] = None


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    status: Optional[str] = None
    project_id: Optional[int] = None
    tags: Optional[List[str]] = None
    dependency_ids: Optional[List[int]] = None


class TaskInDB(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class Task(TaskInDB):
    pass


class TaskWithRelations(TaskInDB):
    tags: List[Tag] = []
    dependencies: List["TaskWithRelations"] = []
    
    class Config:
        orm_mode = True


class TaskDetail(TaskWithRelations):
    dependent_tasks: List[TaskWithRelations] = []


class TaskProblem(BaseModel):
    id: int
    title: str
    status: str
    author: Optional[str] = None
    developer: Optional[str] = None
    tags: List[str] = []
    description: Optional[str] = None
    
    class Config:
        orm_mode = True 