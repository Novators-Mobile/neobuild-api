from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    repository_url: str

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None
    repository_url: Optional[str] = None

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 