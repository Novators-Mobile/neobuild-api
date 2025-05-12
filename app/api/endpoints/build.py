from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from app.db.session import get_db
from app.services.build_release import BuildReleaseService
from app.services.task_validation import TaskValidationService
from app.schemas.release import ReleaseCreate
from app.schemas.task import TaskValidationRequest, TaskValidationResponse
from app.schemas.git import BranchDiff, CommitTransferCheck
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

@router.post("/validate/tasks", response_model=TaskValidationResponse)
def validate_tasks(
    validation_request: TaskValidationRequest
):
    """
    Проверка задач на статусы, зависимости и связи с другими проектами.
    
    Проверяет:
    1. Все задачи должны быть в статусе For Release или In Release
    2. Если задача зависит от другой задачи, зависимая задача также должна быть включена в релиз
    3. Если задачи зависят от других проектов, выводится предупреждение
    
    Возвращает результаты проверки с предупреждениями и списком проблемных задач.
    """
    return TaskValidationService.validate_release_tasks(validation_request.release_task_id)

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

@router.post("/create-branch", response_model=Dict[str, Any])
def create_release_branch(
    release_id: int,
    branch_name: str,
    db: Session = Depends(get_db)
):
    """
    Создание релизной ветки.
    """
    result = BuildReleaseService.create_release_branch(db, release_id, branch_name)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.post("/add-task", response_model=Dict[str, Any])
def add_task_to_release(
    release_id: int,
    task_id: str,
    db: Session = Depends(get_db)
):
    """
    Добавление задачи в релиз.
    """
    result = BuildReleaseService.add_task_to_release(db, release_id, task_id)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.get("/release/{release_id}/diff", response_model=Dict[str, Any])
def get_release_diff(
    release_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение diff между веткой релиза и исходной веткой.
    """
    result = BuildReleaseService.check_branch_diff(db, release_id)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.get("/release/{release_id}/verify-commits", response_model=Dict[str, Any])
def verify_release_commits(
    release_id: int,
    db: Session = Depends(get_db)
):
    """
    Проверка переноса коммитов в ветку релиза.
    """
    result = BuildReleaseService.verify_commits(db, release_id)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.post("/release/{release_id}/complete", response_model=Dict[str, Any])
def complete_release(
    release_id: int,
    db: Session = Depends(get_db)
):
    """
    Завершение релиза после успешной проверки задач и коммитов.
    """
    # Проверяем перенос коммитов
    commit_check = BuildReleaseService.verify_commits(db, release_id)
    if not commit_check["success"]:
        raise HTTPException(status_code=400, detail=commit_check["message"])
    
    # Если не все коммиты перенесены, возвращаем ошибку
    if not commit_check["commit_check"]["all_transferred"]:
        raise HTTPException(status_code=400, detail="Not all commits have been transferred to the release branch")
    
    # Обработка релиза после тестов
    result = BuildReleaseService.process_release_after_tests(db, release_id, "success")
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result