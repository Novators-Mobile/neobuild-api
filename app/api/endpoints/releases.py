from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.crud import release as release_crud, project as project_crud
from app.schemas.release import Release, ReleaseCreate, ReleaseUpdate

router = APIRouter()

@router.get("/", response_model=List[Release])
def read_releases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Получение всех релизов.
    """
    releases = release_crud.get_releases(db, skip=skip, limit=limit)
    return releases

@router.post("/", response_model=Release)
def create_release(
    release: ReleaseCreate,
    db: Session = Depends(get_db)
):
    """
    Создание нового релиза.
    """
    # Проверяем существование проекта
    project = project_crud.get_project(db, project_id=release.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return release_crud.create_release(db=db, release=release)

@router.get("/{release_id}", response_model=Release)
def read_release(
    release_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение конкретного релиза по ID.
    """
    db_release = release_crud.get_release(db, release_id=release_id)
    if db_release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    return db_release

@router.get("/project/{project_id}", response_model=List[Release])
def read_releases_by_project(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Получение всех релизов для конкретного проекта.
    """
    # Проверяем существование проекта
    project = project_crud.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    releases = release_crud.get_releases_by_project(db, project_id=project_id, skip=skip, limit=limit)
    return releases

@router.patch("/{release_id}", response_model=Release)
def update_release(
    release_id: int,
    release_update: ReleaseUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновление релиза.
    """
    db_release = release_crud.get_release(db, release_id=release_id)
    if db_release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    
    # Если project_id обновляется, проверяем существование нового проекта
    if release_update.project_id is not None:
        project = project_crud.get_project(db, project_id=release_update.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Updated project not found")
    
    updated_release = release_crud.update_release(db, release_id=release_id, release_update=release_update)
    return updated_release 