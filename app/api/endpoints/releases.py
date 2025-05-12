from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.session import get_db
from app.crud import release as release_crud, project as project_crud
from app.schemas.release import Release, ReleaseCreate, ReleaseUpdate, ReleaseListResponse
from app.schemas.task import TaskComparison, CommitComparison
from app.schemas.git import BranchDiff, CommitTransferCheck, FileContent
from app.services.issue_tracker import IssueTrackerService
from app.services.git_service import GitService

router = APIRouter()

@router.get("/", response_model=ReleaseListResponse)
def read_releases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Получение всех релизов.
    """
    releases = release_crud.get_releases(db, skip=skip, limit=limit)
    return {"releases": releases}

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

@router.get("/project/{project_id}", response_model=ReleaseListResponse)
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
    return {"releases": releases}

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

@router.get("/{release_id}/task-comparison", response_model=TaskComparison)
def compare_tasks(
    release_id: int,
    db: Session = Depends(get_db)
):
    """
    Сравнение задач в релизе с задачами в новой ветке.
    """
    db_release = release_crud.get_release(db, release_id=release_id)
    if db_release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    
    # Получаем задачи из релиза и из ветки для сравнения
    # Это имитация данных для фронтенда
    return {
        "added_tasks": [{"id": f"TASK-{i}", "title": f"Задача {i}"} for i in range(1, 11)],
        "removed_tasks": [{"id": f"TASK-{i}", "title": f"Задача {i}"} for i in range(4, 7)]
    }

@router.get("/{release_id}/commit-comparison", response_model=CommitComparison)
def compare_commits(
    release_id: int,
    db: Session = Depends(get_db)
):
    """
    Сравнение коммитов в релизе с коммитами в новой ветке.
    """
    db_release = release_crud.get_release(db, release_id=release_id)
    if db_release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    
    # Получаем коммиты из релиза и из ветки для сравнения
    # Это имитация данных для фронтенда
    return {
        "added_commits": [{"id": f"commit-{i}", "message": f"Коммит {i}"} for i in range(1, 11)],
        "removed_commits": [],
        "missing_commits": [{"id": f"commit-{i}", "message": f"Коммит {i}"} for i in range(15, 25)]
    }

@router.get("/{release_id}/diff", response_model=BranchDiff)
def get_release_diff(
    release_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение diff между веткой релиза и исходной веткой.
    """
    db_release = release_crud.get_release(db, release_id=release_id)
    if db_release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    
    # В реальном проекте здесь будет вызов GitService для получения diff
    diff_data = GitService.get_branch_diff(
        project_id=db_release.project_id, 
        branch_from=db_release.branch_from, 
        branch_to=db_release.branch_name
    )
    
    return diff_data

@router.get("/{release_id}/check-commits", response_model=CommitTransferCheck)
def check_commits_transferred(
    release_id: int,
    db: Session = Depends(get_db)
):
    """
    Проверка, все ли коммиты перенесены в релизную ветку.
    """
    db_release = release_crud.get_release(db, release_id=release_id)
    if db_release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    
    # В реальном проекте здесь будет вызов GitService для проверки коммитов
    check_result = GitService.check_commits_transferred(
        project_id=db_release.project_id, 
        branch_from=db_release.branch_from, 
        branch_to=db_release.branch_name
    )
    
    return check_result

@router.get("/{release_id}/file", response_model=FileContent)
def get_file_content(
    release_id: int,
    file_path: str,
    db: Session = Depends(get_db)
):
    """
    Получение содержимого файла из ветки релиза.
    """
    db_release = release_crud.get_release(db, release_id=release_id)
    if db_release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    
    # В реальном проекте здесь будет вызов GitService для получения содержимого файла
    file_content = GitService.get_file_content(
        project_id=db_release.project_id,
        branch=db_release.branch_name,
        file_path=file_path
    )
    
    return file_content 