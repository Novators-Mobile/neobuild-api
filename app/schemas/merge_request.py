from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

from app.models.merge_request import MergeRequestStatus


class MergeRequestStatusEnum(str, Enum):
    OPEN = "open"
    MERGED = "merged"
    CLOSED = "closed"
    CONFLICT = "conflict"


class MergeRequestBase(BaseModel):
    title: str
    description: Optional[str] = None
    source_branch: str
    target_branch: str
    can_be_merged: bool = False
    assigned_to: Optional[str] = None
    task_id: Optional[int] = None
    release_id: Optional[int] = None


class MergeRequestCreate(MergeRequestBase):
    pass


class MergeRequestUpdate(MergeRequestBase):
    title: Optional[str] = None
    status: Optional[MergeRequestStatusEnum] = None
    source_branch: Optional[str] = None
    target_branch: Optional[str] = None


class MergeRequestInDB(MergeRequestBase):
    id: int
    status: MergeRequestStatusEnum
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class MergeRequest(MergeRequestInDB):
    pass 