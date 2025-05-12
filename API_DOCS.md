# API документация для neobuild-api

Документация по API для работы с бэкендом neobuild-api. Все запросы выполняются по базовому URL `/api/v1/`.

## Релизы

### Получение списка релизов

**Запрос:**
```
GET /releases/
```

**Ответ:**
```json
{
  "releases": [
    {
      "id": 1,
      "name": "Название релиза",
      "project_id": 1,
      "release_task_id": "PROJ-1234",
      "branch_from": "develop",
      "branch_name": "release/release-name",
      "skip_pipeline": false,
      "status": "Сделано не завершено",
      "created_at": "2023-01-01T12:00:00Z",
      "updated_at": "2023-01-01T12:00:00Z"
    },
    ...
  ]
}
```

### Получение релиза по ID

**Запрос:**
```
GET /releases/{release_id}
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Название релиза",
  "project_id": 1,
  "release_task_id": "PROJ-1234",
  "branch_from": "develop",
  "branch_name": "release/release-name",
  "skip_pipeline": false,
  "status": "Сделано не завершено",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

### Получение релизов для проекта

**Запрос:**
```
GET /releases/project/{project_id}
```

**Ответ:**
```json
{
  "releases": [
    {
      "id": 1,
      "name": "Название релиза",
      "project_id": 1,
      "release_task_id": "PROJ-1234",
      "branch_from": "develop",
      "branch_name": "release/release-name",
      "skip_pipeline": false,
      "status": "Сделано не завершено",
      "created_at": "2023-01-01T12:00:00Z",
      "updated_at": "2023-01-01T12:00:00Z"
    },
    ...
  ]
}
```

### Создание релиза

**Запрос:**
```
POST /releases/
Content-Type: application/json

{
  "name": "Название релиза",
  "project_id": 1,
  "release_task_id": "PROJ-1234",
  "branch_from": "develop",
  "skip_pipeline": false
}
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Название релиза",
  "project_id": 1,
  "release_task_id": "PROJ-1234",
  "branch_from": "develop",
  "branch_name": "release/release-name",
  "skip_pipeline": false,
  "status": "Сделано не завершено",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

### Обновление релиза

**Запрос:**
```
PATCH /releases/{release_id}
Content-Type: application/json

{
  "name": "Новое название релиза",
  "status": "Готово"
}
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Новое название релиза",
  "project_id": 1,
  "release_task_id": "PROJ-1234",
  "branch_from": "develop",
  "branch_name": "release/release-name",
  "skip_pipeline": false,
  "status": "Готово",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-02T12:00:00Z"
}
```

### Сравнение задач релиза

**Запрос:**
```
GET /releases/{release_id}/task-comparison
```

**Ответ:**
```json
{
  "added_tasks": [
    {
      "id": "TASK-1",
      "title": "Задача 1"
    },
    ...
  ],
  "removed_tasks": [
    {
      "id": "TASK-5",
      "title": "Задача 5"
    },
    ...
  ]
}
```

### Сравнение коммитов релиза

**Запрос:**
```
GET /releases/{release_id}/commit-comparison
```

**Ответ:**
```json
{
  "added_commits": [
    {
      "id": "commit-1",
      "message": "Коммит 1"
    },
    ...
  ],
  "removed_commits": [],
  "missing_commits": [
    {
      "id": "commit-15",
      "message": "Коммит 15"
    },
    ...
  ]
}
```

### Получение diff между ветками

**Запрос:**
```
GET /releases/{release_id}/diff
```

**Ответ:**
```json
{
  "summary": {
    "files_changed": 10,
    "lines_added": 320,
    "lines_removed": 150,
    "diff_too_large": false
  },
  "file_diffs": [
    {
      "filename": "src/component_1.js",
      "status": "modified",
      "additions": 25,
      "deletions": 10,
      "changes": 35,
      "diff_content": "@@ -1,5 +1,10 @@\n+// New code added\n function example() {\n-  // Old code removed\n+  // New implementation\n   return true;\n }}"
    },
    ...
  ]
}
```

### Проверка переноса коммитов

**Запрос:**
```
GET /releases/{release_id}/check-commits
```

**Ответ:**
```json
{
  "all_transferred": false,
  "missing_commits": [
    {
      "id": "abc1234",
      "message": "Fix bug in component 1",
      "author": "user1@example.com",
      "date": "2023-01-01T12:00:00Z"
    },
    ...
  ],
  "message": "There are 3 missing commits"
}
```

### Получение содержимого файла

**Запрос:**
```
GET /releases/{release_id}/file?file_path=src/component.js
```

**Ответ:**
```json
{
  "path": "src/component.js",
  "content": "// This is a sample file content for src/component.js\nfunction example() {\n    console.log(\"Hello, world!\");\n    return 42;\n}\n",
  "size": 113,
  "encoding": "utf-8"
}
```

## Проекты

### Получение списка проектов

**Запрос:**
```
GET /projects/
```

**Ответ:**
```json
[
  {
    "id": 1,
    "name": "Название проекта",
    "description": "Описание проекта",
    "repository_url": "https://github.com/example/repo",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
  },
  ...
]
```

### Получение проекта по ID

**Запрос:**
```
GET /projects/{project_id}
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Название проекта",
  "description": "Описание проекта",
  "repository_url": "https://github.com/example/repo",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

### Создание проекта

**Запрос:**
```
POST /projects/
Content-Type: application/json

{
  "name": "Название проекта",
  "description": "Описание проекта",
  "repository_url": "https://github.com/example/repo"
}
```

**Ответ:**
```json
{
  "id": 1,
  "name": "Название проекта",
  "description": "Описание проекта",
  "repository_url": "https://github.com/example/repo",
  "created_at": "2023-01-01T12:00:00Z",
  "updated_at": "2023-01-01T12:00:00Z"
}
```

## Сборка проекта

### Получение опций для сборки

**Запрос:**
```
GET /build/options
```

**Ответ:**
```json
{
  "projects": [
    {
      "id": 1,
      "name": "Название проекта",
      "description": "Описание проекта",
      "repository_url": "https://github.com/example/repo",
      "created_at": "2023-01-01T12:00:00Z",
      "updated_at": "2023-01-01T12:00:00Z"
    },
    ...
  ],
  "branch_options": ["develop", "main", "feature/some-feature"]
}
```

### Получение задач релиза для проекта

**Запрос:**
```
GET /build/release-tasks/{project_id}
```

**Ответ:**
```json
[
  {
    "id": "PROJ-1234",
    "title": "Release 1.0",
    "description": "Release task for version 1.0",
    "status": "For Release",
    "assignee": "user1@example.com"
  },
  ...
]
```

### Проверка задач релиза

**Запрос:**
```
POST /build/validate/tasks
Content-Type: application/json

{
  "release_task_id": "PROJ-1234"
}
```

**Ответ:**
```json
{
  "success": true,
  "has_errors": true,
  "errors": [
    {
      "error_type": "status",
      "message": "Некоторые задачи имеют недопустимый статус. Допустимые статусы: For Release, In Release.",
      "issues": [
        {
          "id": "PROJ-5678",
          "title": "Task 1",
          "status": "In Progress",
          "tags": ["backend", "bugfix"],
          "author": "user1@example.com",
          "developer": "dev1@example.com"
        },
        ...
      ]
    },
    ...
  ]
}
```

### Инициирование сборки

**Запрос:**
```
POST /build/initiate
Content-Type: application/json

{
  "name": "Название релиза",
  "project_id": 1,
  "release_task_id": "PROJ-1234",
  "branch_from": "develop",
  "skip_pipeline": false
}
```

**Ответ:**
```json
{
  "success": true,
  "release": {
    "id": 1,
    "name": "Название релиза",
    "project_id": 1,
    "release_task_id": "PROJ-1234",
    "branch_from": "develop",
    "branch_name": "release/release-name",
    "skip_pipeline": false,
    "status": "Сделано не завершено",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
  },
  "message": "Release 'Название релиза' created successfully. You can now proceed to the task verification step."
}
```

### Создание релизной ветки

**Запрос:**
```
POST /build/create-branch
Content-Type: application/json

{
  "release_id": 1,
  "branch_name": "release/v1.0"
}
```

**Ответ:**
```json
{
  "success": true,
  "release": {
    "id": 1,
    "name": "Название релиза",
    "project_id": 1,
    "release_task_id": "PROJ-1234",
    "branch_from": "develop",
    "branch_name": "release/v1.0",
    "skip_pipeline": false,
    "status": "Сделано не завершено",
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-02T12:00:00Z"
  },
  "message": "Release branch 'release/v1.0' created successfully."
}
```

### Добавление задачи в релиз

**Запрос:**
```
POST /build/add-task
Content-Type: application/json

{
  "release_id": 1,
  "task_id": "PROJ-5678"
}
```

**Ответ:**
```json
{
  "success": true,
  "message": "Task 'PROJ-5678' added to release 'Название релиза' successfully."
}
```

### Получение diff релиза

**Запрос:**
```
GET /build/release/{release_id}/diff
```

**Ответ:**
```json
{
  "success": true,
  "diff_data": {
    "summary": {
      "files_changed": 8,
      "lines_added": 245,
      "lines_removed": 123,
      "diff_too_large": false
    },
    "file_diffs": [
      {
        "filename": "src/component_1.js",
        "status": "modified",
        "additions": 25,
        "deletions": 10,
        "changes": 35,
        "diff_content": "@@ -1,5 +1,10 @@\n+// New code added\n function example() {\n-  // Old code removed\n+  // New implementation\n   return true;\n }}"
      },
      ...
    ]
  }
}
```

### Проверка переноса коммитов

**Запрос:**
```
GET /build/release/{release_id}/verify-commits
```

**Ответ:**
```json
{
  "success": true,
  "commit_check": {
    "all_transferred": true,
    "missing_commits": [],
    "message": "All commits have been transferred successfully"
  }
}
```

### Завершение релиза

**Запрос:**
```
POST /build/release/{release_id}/complete
```

**Ответ:**
```json
{
  "success": true,
  "message": "Changes automatically merged successfully",
  "merge_result": {
    "success": true,
    "merge_commit_sha": "sha-4563210",
    "message": "Successfully merged develop into release/v1.0"
  }
}
``` 