from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

def get_project(db: Session, project_id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()

def get_project_by_name(db: Session, name: str) -> Optional[Project]:
    return db.query(Project).filter(Project.name == name).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Project]:
    return db.query(Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: ProjectCreate) -> Project:
    db_project = Project(
        name=project.name,
        description=project.description,
        repository_url=project.repository_url
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project 