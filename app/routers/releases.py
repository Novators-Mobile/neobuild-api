from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database.session import get_db
from app.models import Release, Project, Task, Branch
from app.schemas import (
    Release as ReleaseSchema, ReleaseCreate, ReleaseUpdate, 
    ReleaseWithChecks, ReleaseAssemblyResponse
)
from app.routers.auth import get_current_active_user
from app.services.release_service import ReleaseService

router = APIRouter(prefix="/releases", tags=["releases"])


@router.get("/", response_model=List[ReleaseSchema])
def get_releases(
    project_id: int = None,
    status: str = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all releases with optional filters."""
    query = db.query(Release)
    
    if project_id:
        query = query.filter(Release.project_id == project_id)
    if status:
        query = query.filter(Release.status == status)
        
    releases = query.offset(skip).limit(limit).all()
    return releases


@router.get("/{release_id}", response_model=ReleaseWithChecks)
def get_release(
    release_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific release by ID."""
    release = db.query(Release).filter(Release.id == release_id).first()
    if release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    return release


@router.post("/", response_model=ReleaseAssemblyResponse, status_code=status.HTTP_201_CREATED)
def create_release(
    release: ReleaseCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create a new release and perform all necessary checks and operations."""
    project = db.query(Project).filter(Project.id == release.project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    branch = db.query(Branch).filter(Branch.id == release.branch_id).first()
    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")

    # Use the release service to create the release with all checks and operations
    release_service = ReleaseService(db)
    result = release_service.assemble_release(release)
    
    return result


@router.put("/{release_id}", response_model=ReleaseSchema)
def update_release(
    release_id: int, 
    release: ReleaseUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update a release."""
    db_release = db.query(Release).filter(Release.id == release_id).first()
    if db_release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    
    # Check if project exists if changing project
    if release.project_id and release.project_id != db_release.project_id:
        project = db.query(Project).filter(Project.id == release.project_id).first()
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = release.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_release, key, value)
    
    db.commit()
    db.refresh(db_release)
    return db_release


@router.delete("/{release_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_release(
    release_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Delete a release."""
    db_release = db.query(Release).filter(Release.id == release_id).first()
    if db_release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    
    db.delete(db_release)
    db.commit()
    return None


@router.post("/{release_id}/add-task/{task_id}", response_model=Dict[str, Any])
def add_task_to_release(
    release_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Add a task to an existing release."""
    release = db.query(Release).filter(Release.id == release_id).first()
    if release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Use the release service to add the task
    release_service = ReleaseService(db)
    result = release_service.add_task_to_release(release_id, task_id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result


@router.get("/{release_id}/commits", response_model=List[Dict[str, Any]])
def get_release_commits(
    release_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all commits in a release."""
    release = db.query(Release).filter(Release.id == release_id).first()
    if release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    
    release_service = ReleaseService(db)
    commits = release_service.get_release_commits(release_id)
    
    return commits


@router.get("/{release_id}/compare-tasks-commits", response_model=Dict[str, Any])
def compare_tasks_with_commits(
    release_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Compare tasks in the release with commits to ensure all are included."""
    release = db.query(Release).filter(Release.id == release_id).first()
    if release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    
    release_service = ReleaseService(db)
    result = release_service.compare_tasks_with_commits(release_id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result 