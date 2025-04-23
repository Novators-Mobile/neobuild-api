from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.crud import project as project_crud
from app.schemas.project import Project, ProjectCreate

router = APIRouter()

@router.get("/", response_model=List[Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Получение всех проектов.
    """
    projects = project_crud.get_projects(db, skip=skip, limit=limit)
    return projects

@router.post("/", response_model=Project)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Создание нового проекта.
    """
    db_project = project_crud.get_project_by_name(db, name=project.name)
    if db_project:
        raise HTTPException(status_code=400, detail="Project already exists")
    return project_crud.create_project(db=db, project=project)

@router.get("/{project_id}", response_model=Project)
def read_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение конкретного проекта по ID.
    """
    db_project = project_crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project 