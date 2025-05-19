from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CommitBase(BaseModel):
    hash: str
    message: Optional[str] = None
    author: Optional[str] = None
    task_id: Optional[int] = None
    release_id: Optional[int] = None
    branch_name: Optional[str] = None
    in_release: bool = False
    committed_at: Optional[datetime] = None


class CommitCreate(CommitBase):
    pass


class CommitUpdate(CommitBase):
    hash: Optional[str] = None
    in_release: Optional[bool] = None


class CommitInDB(CommitBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class Commit(CommitInDB):
    pass


class CommitDiff(BaseModel):
    old_commit: Optional[Commit] = None
    new_commit: Optional[Commit] = None
    diff_type: str  # added, removed, changed
    line_changes: Optional[dict] = None 