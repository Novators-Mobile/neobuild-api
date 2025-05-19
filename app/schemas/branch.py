from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BranchBase(BaseModel):
    name: str
    is_release_branch: bool = False
    project_id: int


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BranchBase):
    name: Optional[str] = None
    project_id: Optional[int] = None


class BranchInDB(BranchBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True


class Branch(BranchInDB):
    pass 