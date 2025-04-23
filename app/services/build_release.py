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