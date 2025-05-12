from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.release import Release
from app.schemas.release import ReleaseCreate, ReleaseUpdate

def get_release(db: Session, release_id: int) -> Optional[Release]:
    return db.query(Release).filter(Release.id == release_id).first()

def get_releases(db: Session, skip: int = 0, limit: int = 100) -> List[Release]:
    return db.query(Release).offset(skip).limit(limit).all()

def get_releases_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100) -> List[Release]:
    return db.query(Release).filter(Release.project_id == project_id).offset(skip).limit(limit).all()

def create_release(db: Session, release: ReleaseCreate) -> Release:
    # Генерируем имя ветки из имени релиза, если оно не задано
    branch_name = release.branch_name
    if not branch_name:
        branch_name = f"release/{release.name.lower().replace(' ', '-')}"
    
    db_release = Release(
        name=release.name,
        project_id=release.project_id,
        release_task_id=release.release_task_id,
        branch_from=release.branch_from,
        branch_name=branch_name,
        skip_pipeline=release.skip_pipeline,
        status="Сделано не завершено"  # Статус по умолчанию согласно UI
    )
    db.add(db_release)
    db.commit()
    db.refresh(db_release)
    return db_release

def update_release(db: Session, release_id: int, release_update: ReleaseUpdate) -> Optional[Release]:
    db_release = get_release(db, release_id)
    if not db_release:
        return None
    
    update_data = release_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_release, key, value)
        
    db.commit()
    db.refresh(db_release)
    return db_release 