from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models import Project
from app.schemas import Project as ProjectSchema, ProjectCreate, ProjectUpdate
from app.routers.auth import get_current_active_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=List[ProjectSchema])
def get_projects(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all projects."""
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(
    project_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific project by ID."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create a new project."""
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.put("/{project_id}", response_model=ProjectSchema)
def update_project(
    project_id: int, 
    project: ProjectUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update a project."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
        
    update_data = project.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
        
    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Delete a project."""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
        
    db.delete(db_project)
    db.commit()
    return None 