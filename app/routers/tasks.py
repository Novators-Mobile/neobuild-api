from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models import Task, Project, Tag, Branch
from app.schemas import Task as TaskSchema, TaskCreate, TaskUpdate, TaskDetail, TaskProblem
from app.routers.auth import get_current_active_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskSchema])
def get_tasks(
    project_id: int = None,
    branch_id: int = None,
    release_id: int = None,
    is_release_task: bool = None,
    status: str = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all tasks with optional filters."""
    query = db.query(Task)
    
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if branch_id:
        query = query.filter(Task.branch_id == branch_id)
    if release_id:
        query = query.filter(Task.release_id == release_id)
    if is_release_task is not None:
        query = query.filter(Task.is_release_task == is_release_task)
    if status:
        query = query.filter(Task.status == status)
        
    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.get("/{task_id}", response_model=TaskDetail)
def get_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific task by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create a new task."""
    # Check if project exists
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # Check if branch exists if provided
    if task.branch_id:
        branch = db.query(Branch).filter(Branch.id == task.branch_id).first()
        if branch is None:
            raise HTTPException(status_code=404, detail="Branch not found")
    
    # Extract tags and dependencies before creating the task
    tags = task.tags
    dependency_ids = task.dependency_ids
    
    # Create task in the database
    db_task = Task(**task.dict(exclude={"tags", "dependency_ids"}))
    db.add(db_task)
    db.flush()  # To get the ID without committing
    
    # Add tags
    if tags:
        for tag_name in tags:
            # Get or create tag
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()
            db_task.tags.append(tag)
    
    # Add dependencies
    if dependency_ids:
        for dep_id in dependency_ids:
            dep_task = db.query(Task).filter(Task.id == dep_id).first()
            if dep_task:
                db_task.dependencies.append(dep_task)
    
    db.commit()
    db.refresh(db_task)
    return db_task


@router.put("/{task_id}", response_model=TaskSchema)
def update_task(
    task_id: int, 
    task: TaskUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update a task."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if project exists if changing project
    if task.project_id and task.project_id != db_task.project_id:
        project = db.query(Project).filter(Project.id == task.project_id).first()
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if branch exists if changing branch
    if task.branch_id and task.branch_id != db_task.branch_id:
        branch = db.query(Branch).filter(Branch.id == task.branch_id).first()
        if branch is None:
            raise HTTPException(status_code=404, detail="Branch not found")
    
    # Extract tags and dependencies
    tags = task.tags
    dependency_ids = task.dependency_ids
    
    # Update task fields
    update_data = task.dict(exclude={"tags", "dependency_ids"}, exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    # Update tags if provided
    if tags is not None:
        # Clear existing tags
        db_task.tags = []
        
        # Add new tags
        for tag_name in tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.flush()
            db_task.tags.append(tag)
    
    # Update dependencies if provided
    if dependency_ids is not None:
        # Clear existing dependencies
        db_task.dependencies = []
        
        # Add new dependencies
        for dep_id in dependency_ids:
            dep_task = db.query(Task).filter(Task.id == dep_id).first()
            if dep_task:
                db_task.dependencies.append(dep_task)
    
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Delete a task."""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return None


@router.get("/{task_id}/problems", response_model=List[TaskProblem])
def check_task_problems(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Check for problems with a task for release."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    problems = []
    
    # Check for release-related problems
    if task.is_release_task:
        # 1. Check dependencies for correct status
        for dep_task in task.dependencies:
            if dep_task.status not in ["For Release", "In Release"]:
                tag_names = [tag.name for tag in dep_task.tags]
                problems.append(
                    TaskProblem(
                        id=dep_task.id,
                        title=dep_task.title,
                        status=dep_task.status,
                        author=dep_task.author,
                        developer=dep_task.developer,
                        tags=tag_names,
                        description=f"Task is in '{dep_task.status}' status, should be 'For Release' or 'In Release'"
                    )
                )
                
        # 2. Check for dependencies of dependencies not included in release
        for dep_task in task.dependencies:
            for nested_dep in dep_task.dependencies:
                if nested_dep not in task.dependencies and nested_dep != task:
                    tag_names = [tag.name for tag in nested_dep.tags]
                    problems.append(
                        TaskProblem(
                            id=nested_dep.id,
                            title=nested_dep.title,
                            status=nested_dep.status,
                            author=nested_dep.author,
                            developer=nested_dep.developer,
                            tags=tag_names,
                            description=f"Dependency of task #{dep_task.id} is not included in the release"
                        )
                    )
    
    return problems 