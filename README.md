# NeoBuild Backend

Бэкенд-сервис для NeoBuild - автоматизированной системы управления релизами.

## Стек технологий

- FastAPI - Веб-фреймворк
- SQLAlchemy - ORM
- PostgreSQL - База данных
- Docker - Контейнеризация
- JWT - Аутентификация

## Начало работы

### Требования

- Docker и Docker Compose
- Python 3.11+ (для локальной разработки)

### Запуск с Docker

```bash
# Сборка и запуск всех сервисов
docker-compose up -d

# API будет доступно по адресу http://localhost:8000
# Swagger документация по адресу http://localhost:8000/docs
```

### Локальная разработка

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Запустить PostgreSQL (с использованием Docker)
docker-compose up -d db

# Запустить API сервер
uvicorn app.main:app --reload
```

## Документация API и соответствие дизайну

Ниже приведено соответствие между API и экранами в дизайне Figma с детальным описанием полей запросов и ответов.

### Аутентификация

#### Экран входа в систему (admin_authorization)

**Эндпоинт**: `POST /api/v1/auth/token`
- **Запрос**:
  ```json
  {
    "username": "string", // Поле "Логин" в форме
    "password": "string"  // Поле "Пароль" в форме
  }
  ```
- **Ответ**:
  ```json
  {
    "access_token": "string" // JWT токен для последующих запросов
  }
  ```
- **UI элементы**:
  - Поле ввода "Логин" → `username`
  - Поле ввода "Пароль" → `password`
  - Кнопка "Войти" → отправляет запрос на авторизацию

### Проекты (для симуляции работы без интеграции - временно)

#### Список проектов

**Эндпоинт**: `GET /api/v1/projects`
- **Ответ**:
  ```json
  [
    {
      "id": 0,
      "name": "string",
      "description": "string"
    }
  ]
  ```

#### Детали проекта

**Эндпоинт**: `GET /api/v1/projects/{project_id}`
- **Ответ**:
  ```json
  {
    "id": 0,
    "name": "string",
    "description": "string"
  }
  ```

#### Создание проекта

**Эндпоинт**: `POST /api/v1/projects`
- **Запрос**:
  ```json
  {
    "name": "string",
    "description": "string"
  }
  ```

### Ветки

#### Список веток проекта

**Эндпоинт**: `GET /api/v1/branches?project_id={project_id}`
- **Параметры запроса**:
  - `project_id` - ID проекта
- **Ответ**:
  ```json
  [
    {
      "id": 0,
      "name": "string",
      "project_id": 0,
      "is_release_branch": false
    }
  ]
  ```

#### Создание ветки

**Эндпоинт**: `POST /api/v1/branches`
- **Запрос**:
  ```json
  {
    "name": "string",
    "project_id": 0,
    "is_release_branch": false
  }
  ```

### Задачи

#### Список релизных задач

**Эндпоинт**: `GET /api/v1/tasks?project_id={project_id}&is_release_task=true`
- **Параметры запроса**:
  - `project_id` - ID проекта
  - `is_release_task` - фильтр по релизным задачам
- **Ответ**:
  ```json
  [
    {
      "id": 0,
      "title": "string",
      "description": "string",
      "status": "string",
      "author": "string",
      "developer": "string",
      "is_release_task": true,
      "project_id": 0,
      "created_at": "string",
      "updated_at": "string"
    }
  ]
  ```

#### Список задач в релизе

**Эндпоинт**: `GET /api/v1/tasks?release_id={release_id}`
- **Параметры запроса**:
  - `release_id` - ID релиза
- **Ответ**: Аналогичен предыдущему

#### Создание задачи

**Эндпоинт**: `POST /api/v1/tasks`
- **Запрос**:
  ```json
  {
    "title": "string",
    "description": "string",
    "status": "string",
    "author": "string",
    "developer": "string",
    "is_release_task": false,
    "project_id": 0,
    "branch_id": 0,
    "tags": ["string"],
    "dependency_ids": [0]
  }
  ```

#### Проверка проблем с задачей (Экран: admin_task_checking)

**Эндпоинт**: `GET /api/v1/tasks/{task_id}/problems`
- **Параметры пути**:
  - `task_id` - ID задачи
- **Ответ**:
  ```json
  [
    {
      "id": 0,
      "title": "string",     // Заголовок проблемы
      "status": "string",    // Статус задачи
      "author": "string",    // Автор задачи
      "developer": "string", // Разработчик
      "tags": ["string"],    // Теги задачи
      "description": "string" // Описание проблемы
    }
  ]
  ```
- **UI элементы**:
  - Карточка проблемы:
    - "№ Заголовок" → `title`
    - "Статус задачи: XXX" → `status`
    - "Разработчик: XXX" → `developer`
    - "Автор задачи: XXX" → `author`
    - "Теги" → `tags`
    - Красный индикатор ошибки → содержит `description`

### Релизы

#### Список релизов (Экран: admin_home_page)

**Эндпоинт**: `GET /api/v1/releases?project_id={project_id}`
- **Параметры запроса**:
  - `project_id` - ID проекта
- **Ответ**:
  ```json
  [
    {
      "id": 0,
      "name": "string",
      "description": "string",
      "project_id": 0,
      "source_branch_id": 0,
      "created_at": "string",
      "status": "string"
    }
  ]
  ```
- **UI элементы**:
  - Таблица релизов:
    - "Название" → `name`
    - "Описание" → `description`
    - "Дата создания" → `created_at`
    - "Статус" → `status`

#### Создание релиза (Экран: admin_release_assembly)

**Эндпоинт**: `POST /api/v1/releases`
- **Запрос**:
  ```json
  {
    "name": "string",
    "description": "string",
    "project_id": 0,
    "source_branch_id": 0,
    "release_task_id": 0,
    "skip_pipeline": false
  }
  ```
- **UI элементы**:
  - Форма создания релиза:
    - "Название проекта" (выпадающий список) → `project_id`
    - "Релизная задача" (выпадающий список) → `release_task_id`
    - "Ветка" (выпадающий список) → `source_branch_id`
    - "Пропустить пайплайн" (чекбокс) → `skip_pipeline`
  - Уведомления:
    - ✅ "Успех!" → успешное создание релиза
    - 📘 "Уведомление: Ожидайте, идет проверка..." → процесс обработки запроса
    - ❌ "Внимание! Проверка завершена неуспешно." → ошибка при проверке задач
    - 📘 "Внимание! При пропуске пайплайна релиз будет собран без проверок." → предупреждение при `skip_pipeline=true`

#### Добавление задачи в релиз (Экран: admin_add_new_task_to_release)

**Эндпоинт**: `POST /api/v1/releases/{release_id}/add-task/{task_id}`
- **Параметры пути**:
  - `release_id` - ID релиза
  - `task_id` - ID задачи
- **UI элементы**:
  - Форма добавления задачи:
    - "Релизная ветка" (выпадающий список) → используется для определения `release_id`
    - "Название задачи" (выпадающий список) → используется для определения `task_id`
  - Уведомления:
    - Сообщение об успехе/неудаче соответствует статусу ответа

#### Просмотр коммитов в релизе (Экран: admin_release)

**Эндпоинт**: `GET /api/v1/releases/{release_id}/commits`
- **Параметры пути**:
  - `release_id` - ID релиза
- **Ответ**:
  ```json
  [
    {
      "id": "string",
      "message": "string",
      "author": "string",
      "date": "string",
      "branch_name": "string"
    }
  ]
  ```
- **UI элементы**:
  - Секция "Сравнение коммитов":
    - "ID" → `id` (сокращенный хеш коммита)
    - "Сообщение" → `message`
    - "Автор" → `author`
    - "Дата" → `date`
    - "Ветка" → `branch_name`

#### Сравнение задач с коммитами (Экран: admin_release)

**Эндпоинт**: `GET /api/v1/releases/{release_id}/compare-tasks-commits`
- **Параметры пути**:
  - `release_id` - ID релиза
- **Ответ**:
  ```json
  {
    "matched_tasks": [
      {
        "id": 0,
        "title": "string",
        "status": "string"
      }
    ],
    "unmatched_tasks": [
      {
        "id": 0,
        "title": "string",
        "status": "string"
      }
    ],
    "unmatched_commits": [
      {
        "id": "string",
        "message": "string",
        "author": "string"
      }
    ]
  }
  ```
- **UI элементы**:
  - Секция "Сравнение задач":
    - Таблица "Найденные задачи" → `matched_tasks`
    - Таблица "Ненайденные задачи" → `unmatched_tasks`
    - Таблица "Ненайденные коммиты" → `unmatched_commits`

### Создание релизной ветки (Экран: admin_create_release_branch)

**Эндпоинт**: `POST /api/v1/branches`
- **Запрос**:
  ```json
  {
    "name": "string",
    "project_id": 0,
    "is_release_branch": true
  }
  ```
- **UI элементы**:
  - Форма создания релизной ветки:
    - "Название проекта" (выпадающий список) → `project_id`
    - "Название ветки" (поле ввода) → `name`
    - Чекбокс не отображается на UI, но `is_release_branch` автоматически устанавливается в `true` (для симуляции работы без интеграции - временно)
  - Уведомления:
    - Сообщения об успехе/неудаче соответствуют статусу ответа

## Структура базы данных

База данных спроектирована для моделирования всех сущностей в системе управления релизами:

- Projects (Проекты)
- Branches (Ветки)
- Tasks (Задачи)
- Releases (Релизы)
- Commits (Коммиты)
- Tags (Теги)
