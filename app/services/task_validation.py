from typing import Dict, Any, List

from app.services.issue_tracker import IssueTrackerService
from app.schemas.task import TaskValidationError, TaskValidationIssue, TaskValidationResponse

class TaskValidationService:
    """
    Сервис для валидации задач релиза.
    """
    
    @staticmethod
    def validate_release_tasks(release_task_id: str) -> TaskValidationResponse:
        """
        Проверка задач на 3 типа ошибок:
        1. Статусы задач должны быть For Release или In Release
        2. Все зависимые задачи должны быть включены в релиз
        3. Предупреждение о зависимостях от других проектов
        
        Args:
            release_task_id: ID задачи релиза
            
        Returns:
            Объект с результатами валидации
        """
        # Получаем задачи, связанные с релизом
        tasks = IssueTrackerService.get_tasks_by_release(release_task_id)
        
        errors = []
        
        # 1. Проверка статусов задач
        status_valid, invalid_status_tasks = IssueTrackerService.validate_task_statuses(tasks)
        
        if not status_valid:
            status_error = TaskValidationError(
                error_type="status",
                message="Некоторые задачи имеют недопустимый статус. Допустимые статусы: For Release, In Release.",
                issues=[
                    TaskValidationIssue(
                        id=task["id"],
                        title=task["title"],
                        status=task["status"],
                        tags=task.get("tags"),
                        author=task.get("author"),
                        developer=task.get("developer")
                    ) for task in invalid_status_tasks
                ]
            )
            errors.append(status_error)
        
        # 2. Проверка зависимостей задач
        deps_valid, tasks_with_missing_deps = IssueTrackerService.validate_task_dependencies(tasks)
        
        if not deps_valid:
            deps_error = TaskValidationError(
                error_type="dependency",
                message="Некоторые задачи имеют зависимости, которые не включены в релиз.",
                issues=[]
            )
            
            for task in tasks_with_missing_deps:
                missing_deps = task.get("missing_dependencies", [])
                for dep in missing_deps:
                    deps_error.issues.append(
                        TaskValidationIssue(
                            id=dep["id"],
                            title=dep["title"],
                            status=dep["status"],
                            tags=dep.get("tags"),
                            author=dep.get("author"),
                            developer=dep.get("developer")
                        )
                    )
            
            errors.append(deps_error)
        
        # 3. Проверка зависимостей от других проектов
        _, tasks_with_project_deps = IssueTrackerService.validate_project_dependencies(tasks)
        
        if tasks_with_project_deps:
            project_deps_error = TaskValidationError(
                error_type="project_dependency",
                message="Предупреждение: Некоторые задачи имеют зависимости от других проектов.",
                issues=[]
            )
            
            for task in tasks_with_project_deps:
                project_deps = task.get("project_dependencies", [])
                for dep in project_deps:
                    project_deps_error.issues.append(
                        TaskValidationIssue(
                            id=dep["id"],
                            title=dep["title"],
                            status=dep["status"],
                            tags=dep.get("tags"),
                            author=dep.get("author"),
                            developer=dep.get("developer")
                        )
                    )
            
            errors.append(project_deps_error)
        
        # Формируем итоговый ответ
        return TaskValidationResponse(
            success=True,
            has_errors=len(errors) > 0,
            errors=errors
        ) 