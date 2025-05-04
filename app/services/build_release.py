from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.crud import project as project_crud, release as release_crud
from app.schemas.release import ReleaseCreate
from app.services.issue_tracker import IssueTrackerService

class BuildReleaseService:
    """
    Сервис для обработки первого этапа процесса создания релиза.
    """
    
    @staticmethod
    def get_build_options(db: Session) -> Dict[str, Any]:
        """
        Получение опций для первого этапа создания релиза.
        
        Returns:
            Словарь с проектами и опциями ветвей.
        """
        # Получаем все проекты для выбора
        projects = project_crud.get_projects(db)
        
        # Примеры опций ветвей (в реальном сценарии они будут приходить из Git)
        branch_options = ["develop", "main", "feature/some-feature"]
        
        return {
            "projects": projects,
            "branch_options": branch_options
        }
    
    @staticmethod
    def get_release_tasks(project_id: int) -> List[Dict[str, Any]]:
        """
        Получение задач релиза для проекта.
        
        Args:
            project_id: ID проекта
            
        Returns:
            Список задач релиза
        """
        return IssueTrackerService.get_release_tasks(project_id)
    
    @staticmethod
    def create_initial_release(db: Session, release_data: ReleaseCreate) -> Dict[str, Any]:
        """
        Создание начального релиза на основе выбора первого этапа.
        
        Args:
            db: Сессия базы данных
            release_data: Данные для создания релиза
            
        Returns:
            Словарь с созданным релизом и статусом успеха
        """
        # Создаем новый релиз
        release = release_crud.create_release(db, release_data)
        
        return {
            "success": True,
            "release": release,
            "message": f"Release '{release.name}' created successfully. You can now proceed to the task verification step."
        }

    @staticmethod
    def process_release_after_tests(db: Session, release_id: int, pipeline_status: str) -> Dict[str, Any]:
        """
        Обработка релизной ветки после успешного прохождения тестов.
        
        Args:
            db: Сессия базы данных
            release_id: ID релиза
            pipeline_status: Статус pipeline
            
        Returns:
            Словарь с результатом обработки
        """
        # Получаем информацию о релизе
        release = release_crud.get_release(db, release_id)
        if not release:
            return {
                "success": False,
                "message": "Release not found"
            }

        # Проверяем статус pipeline
        if pipeline_status != "success":
            return {
                "success": False,
                "message": "Pipeline tests have not passed successfully"
            }

        try:
            # Проверяем возможность автоматического слияния
            can_auto_merge = IssueTrackerService.check_auto_merge_possibility(
                project_id=release.project_id,
                source_branch=release.source_branch,
                target_branch=release.release_branch
            )

            if can_auto_merge:
                # Выполняем автоматическое слияние
                merge_result = IssueTrackerService.merge_branches(
                    project_id=release.project_id,
                    source_branch=release.source_branch,
                    target_branch=release.release_branch
                )
                
                return {
                    "success": True,
                    "message": "Changes automatically merged successfully",
                    "merge_result": merge_result
                }
            else:
                # Создаем задачу для релиз-менеджера
                task_data = {
                    "title": f"Manual merge required for release {release.name}",
                    "description": f"Please review and merge changes from {release.source_branch} to {release.release_branch}",
                    "project_id": release.project_id,
                    "type": "Task",
                    "priority": "High"
                }
                
                task = IssueTrackerService.create_task(task_data)
                
                return {
                    "success": True,
                    "message": "Task created for release manager",
                    "task": task
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error processing release: {str(e)}"
            } 