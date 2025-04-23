from typing import Dict, Any, List
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