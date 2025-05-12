from typing import Dict, Any, List
import random

class GitService:
    """
    Сервис для взаимодействия с Git репозиториями.
    В реальной реализации здесь были бы API-вызовы к системе контроля версий (GitHub, GitLab, Bitbucket и т.д.)
    """
    
    @staticmethod
    def get_branch_diff(project_id: int, branch_from: str, branch_to: str) -> Dict[str, Any]:
        """
        Получение diff между двумя ветками.
        
        Args:
            project_id: ID проекта
            branch_from: Исходная ветка
            branch_to: Целевая ветка
            
        Returns:
            Словарь с результатами diff
        """
        # В реальном сценарии здесь был бы вызов API Git для получения diff
        
        # Имитация данных
        files_changed = random.randint(5, 15)
        lines_added = random.randint(100, 500)
        lines_removed = random.randint(50, 200)
        
        # Генерируем примеры файлов с изменениями
        file_diffs = []
        for i in range(files_changed):
            file_type = random.choice(['js', 'py', 'css', 'html', 'json'])
            filename = f"src/component_{i}.{file_type}"
            
            file_diffs.append({
                "filename": filename,
                "status": random.choice(['modified', 'added', 'deleted']),
                "additions": random.randint(5, 50),
                "deletions": random.randint(0, 30),
                "changes": random.randint(10, 80),
                "diff_content": f"@@ -1,5 +1,10 @@\n+// New code added\n function example() {{\n-  // Old code removed\n+  // New implementation\n   return true;\n }}"
            })
        
        return {
            "summary": {
                "files_changed": files_changed,
                "lines_added": lines_added,
                "lines_removed": lines_removed,
                "diff_too_large": files_changed > 10  # Если diff слишком большой
            },
            "file_diffs": file_diffs
        }
    
    @staticmethod
    def check_commits_transferred(project_id: int, branch_from: str, branch_to: str) -> Dict[str, Any]:
        """
        Проверка, все ли коммиты перенесены из одной ветки в другую.
        
        Args:
            project_id: ID проекта
            branch_from: Исходная ветка
            branch_to: Целевая ветка
            
        Returns:
            Словарь с результатами проверки
        """
        # В реальном сценарии здесь был бы вызов API Git для проверки коммитов
        
        # Генерируем случайный результат
        all_transferred = random.choice([True, False])
        
        missing_commits = []
        if not all_transferred:
            # Генерируем список отсутствующих коммитов
            missing_count = random.randint(1, 5)
            for i in range(missing_count):
                commit_hash = ''.join(random.choices('0123456789abcdef', k=7))
                missing_commits.append({
                    "id": commit_hash,
                    "message": f"Fix bug in component {i}",
                    "author": f"user{random.randint(1, 5)}@example.com",
                    "date": "2023-01-01T12:00:00Z"
                })
        
        return {
            "all_transferred": all_transferred,
            "missing_commits": missing_commits,
            "message": "All commits have been transferred successfully" if all_transferred else 
                        f"There are {len(missing_commits)} missing commits"
        }
    
    @staticmethod
    def get_file_content(project_id: int, branch: str, file_path: str) -> Dict[str, Any]:
        """
        Получение содержимого файла из ветки.
        
        Args:
            project_id: ID проекта
            branch: Ветка
            file_path: Путь к файлу
            
        Returns:
            Словарь с содержимым файла
        """
        # В реальном сценарии здесь был бы вызов API Git для получения содержимого файла
        
        content = f"""
        // This is a sample file content for {file_path}
        function example() {{
            console.log("Hello, world!");
            return 42;
        }}
        """
        
        return {
            "path": file_path,
            "content": content,
            "size": len(content),
            "encoding": "utf-8"
        } 