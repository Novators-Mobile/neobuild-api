from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TaskBase(BaseModel):
    id: str
    title: str
    status: str
    
class TaskDetail(TaskBase):
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    developer: Optional[str] = None
    problem_description: Optional[str] = None  # Для "Описание проблемы" в UI
    
class TaskValidationRequest(BaseModel):
    release_task_id: str
    
class TaskValidationIssue(BaseModel):
    id: str
    title: str
    status: str
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    developer: Optional[str] = None
    
class TaskValidationError(BaseModel):
    error_type: str  # "status", "dependency", "project_dependency"
    message: str
    issues: List[TaskValidationIssue] = []
    
class TaskValidationResponse(BaseModel):
    success: bool
    has_errors: bool
    errors: List[TaskValidationError] = []

class TaskComparisonItem(BaseModel):
    id: str
    title: str
    
class TaskComparison(BaseModel):
    added_tasks: List[TaskComparisonItem] = []
    removed_tasks: List[TaskComparisonItem] = []
    
class CommitComparisonItem(BaseModel):
    id: str
    message: str
    
class CommitComparison(BaseModel):
    added_commits: List[CommitComparisonItem] = []
    removed_commits: List[CommitComparisonItem] = []
    missing_commits: List[CommitComparisonItem] = [] 