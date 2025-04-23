from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReleaseBase(BaseModel):
    name: str
    project_id: int
    release_task_id: str
    branch_from: str
    skip_pipeline: bool = False

class ReleaseCreate(ReleaseBase):
    pass

class ReleaseUpdate(BaseModel):
    name: Optional[str] = None
    project_id: Optional[int] = None
    release_task_id: Optional[str] = None
    branch_from: Optional[str] = None
    branch_name: Optional[str] = None
    skip_pipeline: Optional[bool] = None
    status: Optional[str] = None

class Release(ReleaseBase):
    id: int
    branch_name: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ReleaseInDB(Release):
    pass 