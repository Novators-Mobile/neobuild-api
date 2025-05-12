from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base

class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    release_task_id = Column(String, index=True)  # ID задачи в системе отслеживания задач
    branch_name = Column(String)
    branch_from = Column(String)
    skip_pipeline = Column(Boolean, default=False)
    status = Column(String, default="Сделано не завершено")  # Изменен в соответствии с UI
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связь
    project = relationship("Project", back_populates="releases") 