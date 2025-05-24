from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

from app.models.release import ReleaseStatus


class ReleaseStatusEnum(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class CheckStatusEnum(str, Enum):
    SUCCESS = "success"
    WARNING = "warning" 
    ERROR = "error"


class ReleaseBase(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: int
    branch_id: Optional[int] = None
    skip_pipeline: bool = False


class ReleaseCreate(ReleaseBase):
    pass


class ReleaseUpdate(ReleaseBase):
    name: Optional[str] = None
    status: Optional[ReleaseStatusEnum] = None
    project_id: Optional[int] = None


class ReleaseCheckBase(BaseModel):
    release_id: int
    check_type: str
    status: str
    message: Optional[str] = None
    details: Optional[str] = None


class ReleaseCheckCreate(ReleaseCheckBase):
    pass


class ReleaseCheckInDB(ReleaseCheckBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class ReleaseCheck(ReleaseCheckInDB):
    pass


class ReleaseInDB(ReleaseBase):
    id: int
    status: ReleaseStatusEnum
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class Release(ReleaseInDB):
    pass


class ReleaseWithChecks(Release):
    checks: List[ReleaseCheck] = []


class ReleaseTaskCheck(BaseModel):
    task_id: int
    title: str
    status: str
    author: Optional[str] = None
    developer: Optional[str] = None
    tags: List[str] = []
    problem: Optional[str] = None


class ReleaseAssemblyResponse(BaseModel):
    success: bool
    message: str
    release_id: Optional[int] = None
    checks: List[Dict[str, Any]] = []


class ReleaseBranchResponse(BaseModel):
    success: bool
    message: str
    branch_id: Optional[int] = None
    branch_name: Optional[str] = None


class ReleaseTaskDependencyCheck(BaseModel):
    task_id: int
    title: str
    dependency_id: int
    dependency_title: str
    in_release: bool


class ReleaseCommitCheck(BaseModel):
    task_id: int
    task_title: str
    commit_hash: str
    commit_message: str
    in_release: bool 