from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class FileDiff(BaseModel):
    filename: str
    status: str  # 'modified', 'added', 'deleted'
    additions: int
    deletions: int
    changes: int
    diff_content: str

class DiffSummary(BaseModel):
    files_changed: int
    lines_added: int
    lines_removed: int
    diff_too_large: bool = False

class BranchDiff(BaseModel):
    summary: DiffSummary
    file_diffs: List[FileDiff]

class Commit(BaseModel):
    id: str
    message: str
    author: Optional[str] = None
    date: Optional[str] = None

class CommitTransferCheck(BaseModel):
    all_transferred: bool
    missing_commits: List[Commit] = []
    message: str

class FileContent(BaseModel):
    path: str
    content: str
    size: int
    encoding: str = "utf-8" 