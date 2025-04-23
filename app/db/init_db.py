from sqlalchemy.orm import Session

from app.db.base import Base, engine
from app.models import project, release

# Импорт всех моделей
# Необходимо для работы Base.metadata.create_all()

def init_db() -> None:
    # Создание таблиц
    Base.metadata.create_all(bind=engine) 