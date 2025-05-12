from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.crud import project as project_crud, release as release_crud
from app.schemas.release import ReleaseCreate, ReleaseUpdate
from app.services.issue_tracker import IssueTrackerService
from app.services.git_service import GitService

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
    def create_release_branch(db: Session, release_id: int, branch_name: str) -> Dict[str, Any]:
        """
        Создание релизной ветки.
        
        Args:
            db: Сессия базы данных
            release_id: ID релиза
            branch_name: Имя ветки
            
        Returns:
            Словарь с результатом создания ветки
        """
        # Получаем информацию о релизе
        release = release_crud.get_release(db, release_id)
        if not release:
            return {
                "success": False,
                "message": "Release not found"
            }
        
        # Обновляем имя ветки релиза и сохраняем
        release_update = ReleaseUpdate(branch_name=branch_name)
        updated_release = release_crud.update_release(db, release_id, release_update)
        
        # В реальном сценарии здесь был бы вызов Git API для создания ветки
        
        return {
            "success": True,
            "release": updated_release,
            "message": f"Release branch '{branch_name}' created successfully."
        }
    
    @staticmethod
    def add_task_to_release(db: Session, release_id: int, task_id: str) -> Dict[str, Any]:
        """
        Добавление задачи в релиз.
        
        Args:
            db: Сессия базы данных
            release_id: ID релиза
            task_id: ID задачи
            
        Returns:
            Словарь с результатом добавления задачи
        """
        # Получаем информацию о релизе
        release = release_crud.get_release(db, release_id)
        if not release:
            return {
                "success": False,
                "message": "Release not found"
            }
        
        # В реальном сценарии здесь был бы вызов API трекера задач для привязки задачи к релизу
        # Имитируем успешный результат
        
        return {
            "success": True,
            "message": f"Task '{task_id}' added to release '{release.name}' successfully."
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
                source_branch=release.branch_from,
                target_branch=release.branch_name
            )

            if can_auto_merge:
                # Выполняем автоматическое слияние
                merge_result = IssueTrackerService.merge_branches(
                    project_id=release.project_id,
                    source_branch=release.branch_from,
                    target_branch=release.branch_name
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
                    "description": f"Please review and merge changes from {release.branch_from} to {release.branch_name}",
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
    
    @staticmethod
    def check_branch_diff(db: Session, release_id: int) -> Dict[str, Any]:
        """
        Проверка diff между ветками.
        
        Args:
            db: Сессия базы данных
            release_id: ID релиза
            
        Returns:
            Словарь с результатами diff
        """
        # Получаем информацию о релизе
        release = release_crud.get_release(db, release_id)
        if not release:
            return {
                "success": False,
                "message": "Release not found"
            }
        
        # Получаем diff между ветками
        diff_data = GitService.get_branch_diff(
            project_id=release.project_id,
            branch_from=release.branch_from,
            branch_to=release.branch_name
        )
        
        return {
            "success": True,
            "diff_data": diff_data
        }
    
    @staticmethod
    def verify_commits(db: Session, release_id: int) -> Dict[str, Any]:
        """
        Проверка переноса коммитов.
        
        Args:
            db: Сессия базы данных
            release_id: ID релиза
            
        Returns:
            Словарь с результатами проверки коммитов
        """
        # Получаем информацию о релизе
        release = release_crud.get_release(db, release_id)
        if not release:
            return {
                "success": False,
                "message": "Release not found"
            }
        
        # Проверяем перенос коммитов
        commit_check = GitService.check_commits_transferred(
            project_id=release.project_id,
            branch_from=release.branch_from,
            branch_to=release.branch_name
        )
        
        return {
            "success": True,
            "commit_check": commit_check
        } 