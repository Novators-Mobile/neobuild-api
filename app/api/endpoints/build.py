from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.db.session import get_db
from app.services.build_release import BuildReleaseService
from app.schemas.release import ReleaseCreate
from app.utils.validators import validate_branch_name, validate_release_name

router = APIRouter()

@router.get("/options", response_model=Dict[str, Any])
def get_build_options(
    db: Session = Depends(get_db)
):
    """
    Получение опций для первого этапа создания релиза.
    Возвращает список проектов и опции ветвей.
    """
    return BuildReleaseService.get_build_options(db)

@router.get("/release-tasks/{project_id}", response_model=List[Dict[str, Any]])
def get_release_tasks(
    project_id: int
):
    """
    Получение задач релиза для конкретного проекта.
    Используется для заполнения выпадающего списка задач релиза в пользовательском интерфейсе.
    """
    return BuildReleaseService.get_release_tasks(project_id)

@router.get("/validate/branch-name/{branch_name}", response_model=Dict[str, Any])
def validate_branch(
    branch_name: str
):
    """
    Проверка имени ветки.
    """
    return validate_branch_name(branch_name)

@router.get("/validate/release-name/{release_name}", response_model=Dict[str, Any])
def validate_release(
    release_name: str
):
    """
    Проверка имени релиза.
    """
    return validate_release_name(release_name)

@router.post("/initiate", response_model=Dict[str, Any])
def initiate_build(
    release_data: ReleaseCreate,
    db: Session = Depends(get_db)
):
    """
    Инициирование первого этапа создания релиза.
    Создает релиз с выбранным проектом, задачей, веткой и опцией конвейера.
    """
    # Проверка входных данных
    branch_validation = validate_branch_name(release_data.branch_from)
    release_validation = validate_release_name(release_data.name)
    
    errors = []
    
    if not branch_validation["valid"]:
        errors.extend(branch_validation["errors"])
    
    if not release_validation["valid"]:
        errors.extend(release_validation["errors"])
    
    if errors:
        raise HTTPException(status_code=400, detail={"errors": errors})
    
    return BuildReleaseService.create_initial_release(db, release_data)