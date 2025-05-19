from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models import Branch, Project
from app.schemas import Branch as BranchSchema, BranchCreate, BranchUpdate
from app.routers.auth import get_current_active_user

router = APIRouter(prefix="/branches", tags=["branches"])


@router.get("/", response_model=List[BranchSchema])
def get_branches(
    project_id: int = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all branches, optionally filtered by project."""
    query = db.query(Branch)
    if project_id:
        query = query.filter(Branch.project_id == project_id)
    branches = query.offset(skip).limit(limit).all()
    return branches


@router.get("/{branch_id}", response_model=BranchSchema)
def get_branch(
    branch_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific branch by ID."""
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch


@router.post("/", response_model=BranchSchema, status_code=status.HTTP_201_CREATED)
def create_branch(
    branch: BranchCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create a new branch."""
    # Check if project exists
    project = db.query(Project).filter(Project.id == branch.project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # Create branch in the database
    db_branch = Branch(**branch.dict())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch


@router.put("/{branch_id}", response_model=BranchSchema)
def update_branch(
    branch_id: int, 
    branch: BranchUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update a branch."""
    db_branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
        
    # Check if project exists if changing project
    if branch.project_id and branch.project_id != db_branch.project_id:
        project = db.query(Project).filter(Project.id == branch.project_id).first()
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
            
    update_data = branch.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_branch, key, value)
        
    db.commit()
    db.refresh(db_branch)
    return db_branch


@router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(
    branch_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Delete a branch."""
    db_branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    db.delete(db_branch)
    db.commit()
    return None 