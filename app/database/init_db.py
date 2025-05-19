import logging
from sqlalchemy.orm import Session

from app.database.session import SessionLocal, engine, Base
from app.models import Project, Branch, Task, Tag, TaskStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    """Initialize the database with some example data."""
    db = SessionLocal()
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Check if we already have some data
        if db.query(Project).count() > 0:
            logger.info("Database already contains data, skipping initialization")
            return
        
        # Create example project
        project = Project(
            name="Example Project",
            description="This is an example project",
            gitlab_project_id="123456",
            youtrack_project_id="EXP"
        )
        db.add(project)
        db.flush()
        
        # Create branches
        develop_branch = Branch(
            name="develop",
            project_id=project.id,
            is_release_branch=False
        )
        db.add(develop_branch)
        
        feature_branch = Branch(
            name="feature/new-feature",
            project_id=project.id,
            is_release_branch=False
        )
        db.add(feature_branch)
        db.flush()
        
        # Create tags
        important_tag = Tag(name="важное")
        urgent_tag = Tag(name="срочное")
        critical_tag = Tag(name="критическийфикс")
        db.add(important_tag)
        db.add(urgent_tag)
        db.add(critical_tag)
        db.flush()
        
        # Create release task
        release_task = Task(
            title="Release 1.0.0",
            description="First major release",
            youtrack_id="EXP-1",
            status=TaskStatus.FOR_RELEASE.value,
            author="Иванов Иван Иванович",
            developer="Иванов Иван Иванович",
            is_release_task=True,
            project_id=project.id
        )
        release_task.tags.append(important_tag)
        db.add(release_task)
        db.flush()
        
        # Create feature tasks
        task1 = Task(
            title="Implement login",
            description="Implement user authentication",
            youtrack_id="EXP-2",
            status=TaskStatus.FOR_RELEASE.value,
            author="Иванов Иван Иванович",
            developer="Петров Петр Петрович",
            is_release_task=False,
            project_id=project.id,
            branch_id=feature_branch.id
        )
        task1.tags.append(important_tag)
        db.add(task1)
        
        task2 = Task(
            title="Implement dashboard",
            description="Create user dashboard",
            youtrack_id="EXP-3",
            status=TaskStatus.FOR_RELEASE.value,
            author="Иванов Иван Иванович",
            developer="Сидоров Сидор Сидорович",
            is_release_task=False,
            project_id=project.id,
            branch_id=feature_branch.id
        )
        task2.tags.extend([important_tag, urgent_tag])
        db.add(task2)
        
        # Add dependencies
        release_task.dependencies.append(task1)
        release_task.dependencies.append(task2)
        
        db.commit()
        logger.info("Database initialized with example data")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Initializing database")
    init_db()
    logger.info("Database initialization completed") 