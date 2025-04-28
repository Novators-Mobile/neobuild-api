from typing import Dict, Any, List, Tuple
import random

class IssueTrackerService:
    """
    Сервис для взаимодействия с системой отслеживания задач (например, YouTrack).
    Это симуляция для целей разработки.
    В реальной реализации здесь были бы API-вызовы к фактической системе отслеживания задач.
    """
    
    @staticmethod
    def get_release_tasks(project_id: int) -> List[Dict[str, Any]]:
        """
        Получение задач релиза для проекта.
        
        Args:
            project_id: ID проекта
            
        Returns:
            Список задач релиза
        """
        # В реальном сценарии здесь был бы вызов API YouTrack
        # Пока генерируем примеры данных
        
        # Генерируем 5-10 случайных задач релиза
        num_tasks = random.randint(5, 10)
        
        tasks = []
        for i in range(num_tasks):
            task_id = f"PROJ-{random.randint(1000, 9999)}"
            tasks.append({
                "id": task_id,
                "title": f"Release {i+1}.0",
                "description": f"Release task for version {i+1}.0",
                "status": random.choice(["For Release", "In Release", "Released", "In Progress"]),
                "assignee": f"user{random.randint(1, 5)}@example.com"
            })
            
        return tasks
    
    @staticmethod
    def get_tasks_by_release(release_task_id: str) -> List[Dict[str, Any]]:
        """
        Получение задач, связанных с задачей релиза.
        
        Args:
            release_task_id: ID задачи релиза
            
        Returns:
            Список задач
        """
        # В реальном сценарии здесь был бы вызов API YouTrack
        # Пока генерируем примеры данных
        
        # Генерируем 10-20 случайных задач
        num_tasks = random.randint(10, 20)
        
        tasks = []
        for i in range(num_tasks):
            task_id = f"PROJ-{random.randint(1000, 9999)}"
            status = random.choice(["For Release", "In Release", "In Progress", "To Do", "Done"])
            
            tasks.append({
                "id": task_id,
                "title": f"Task {i+1}",
                "description": f"Description for task {i+1}",
                "status": status,
                "tags": random.sample(["backend", "frontend", "bugfix", "feature", "optimization"], k=random.randint(1, 3)),
                "author": f"user{random.randint(1, 5)}@example.com",
                "developer": f"dev{random.randint(1, 10)}@example.com"
            })
            
        return tasks

    @staticmethod
    def get_task_dependencies(task_id: str) -> List[Dict[str, Any]]:
        """
        Получение зависимостей задачи.
        
        Args:
            task_id: ID задачи
            
        Returns:
            Список зависимых задач
        """
        # В реальном сценарии здесь был бы вызов API YouTrack
        # Пока генерируем примеры данных с вероятностью 30% наличия зависимостей
        
        if random.random() > 0.7:
            num_deps = random.randint(1, 3)
            deps = []
            
            for i in range(num_deps):
                dep_id = f"PROJ-{random.randint(1000, 9999)}"
                deps.append({
                    "id": dep_id,
                    "title": f"Dependency Task {i+1}",
                    "status": random.choice(["For Release", "In Release", "In Progress", "To Do", "Done"]),
                    "tags": random.sample(["backend", "frontend", "bugfix", "feature", "optimization"], k=random.randint(1, 3)),
                    "author": f"user{random.randint(1, 5)}@example.com",
                    "developer": f"dev{random.randint(1, 10)}@example.com"
                })
            
            return deps
        
        return []
    
    @staticmethod
    def get_project_dependencies(task_id: str) -> List[Dict[str, Any]]:
        """
        Получение зависимостей задачи от других проектов.
        
        Args:
            task_id: ID задачи
            
        Returns:
            Список зависимостей от других проектов
        """
        # В реальном сценарии здесь был бы вызов API YouTrack
        # Пока генерируем примеры данных с вероятностью 20% наличия зависимостей от других проектов
        
        if random.random() > 0.8:
            num_deps = random.randint(1, 2)
            deps = []
            
            projects = ["BACKEND", "FRONTEND", "MOBILE", "ADMIN", "API"]
            
            for i in range(num_deps):
                project = random.choice(projects)
                dep_id = f"{project}-{random.randint(1000, 9999)}"
                deps.append({
                    "id": dep_id,
                    "title": f"Project Dependency {i+1}",
                    "project": project,
                    "status": random.choice(["For Release", "In Release", "In Progress", "To Do", "Done"]),
                    "tags": random.sample(["backend", "frontend", "bugfix", "feature", "optimization"], k=random.randint(1, 2)),
                    "author": f"user{random.randint(1, 5)}@example.com",
                    "developer": f"dev{random.randint(1, 10)}@example.com"
                })
            
            return deps
        
        return []
    
    @staticmethod
    def validate_task_statuses(tasks: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Проверка статусов задач - должны быть в 'For Release' или 'In Release'.
        
        Args:
            tasks: Список задач
            
        Returns:
            Tuple из (валидность, список задач с ошибками)
        """
        valid_statuses = ["For Release", "In Release"]
        invalid_tasks = [task for task in tasks if task["status"] not in valid_statuses]
        
        return len(invalid_tasks) == 0, invalid_tasks
    
    @staticmethod
    def validate_task_dependencies(tasks: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Проверка зависимостей задач - все зависимые задачи должны быть в релизе.
        
        Args:
            tasks: Список задач
            
        Returns:
            Tuple из (валидность, список задач с проблемными зависимостями)
        """
        task_ids = {task["id"] for task in tasks}
        tasks_with_missing_deps = []
        
        for task in tasks:
            dependencies = IssueTrackerService.get_task_dependencies(task["id"])
            
            # Проверяем, все ли зависимости включены в релиз
            missing_dependencies = [dep for dep in dependencies if dep["id"] not in task_ids]
            
            if missing_dependencies:
                task_with_deps = task.copy()
                task_with_deps["missing_dependencies"] = missing_dependencies
                tasks_with_missing_deps.append(task_with_deps)
        
        return len(tasks_with_missing_deps) == 0, tasks_with_missing_deps
    
    @staticmethod
    def validate_project_dependencies(tasks: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Проверка зависимостей от других проектов.
        
        Args:
            tasks: Список задач
            
        Returns:
            Tuple из (валидность, список задач с зависимостями от других проектов)
        """
        tasks_with_project_deps = []
        
        for task in tasks:
            project_dependencies = IssueTrackerService.get_project_dependencies(task["id"])
            
            if project_dependencies:
                task_with_deps = task.copy()
                task_with_deps["project_dependencies"] = project_dependencies
                tasks_with_project_deps.append(task_with_deps)
        
        # Даже если есть зависимости от других проектов, это не является ошибкой,
        # но мы всё равно сообщаем о них как о предупреждении
        return True, tasks_with_project_deps 