from typing import List, Dict, Any, Optional, Tuple
import json
import logging
from sqlalchemy.orm import Session

from app.models import Project, Release, Branch, Task, ReleaseCheck, MergeRequest, Commit
from app.models.task import TaskStatus
from app.models.release import ReleaseStatus
from app.models.merge_request import MergeRequestStatus
from app.schemas import (
    ReleaseCreate, ReleaseTaskCheck, ReleaseAssemblyResponse, 
    ReleaseBranchResponse, ReleaseTaskDependencyCheck, CheckStatusEnum
)

logger = logging.getLogger(__name__)


class ReleaseService:
    def __init__(self, db: Session):
        self.db = db

    def check_task_statuses(self, release_task_id: int) -> Tuple[List[ReleaseTaskCheck], bool]:
        """Check if all tasks related to the release task have the correct status."""
        release_task = self.db.query(Task).filter(Task.id == release_task_id).first()
        if not release_task:
            return [], False

        # Get all tasks that are dependencies of the release task
        tasks = []
        for task in release_task.dependencies:
            tasks.append(task)

        task_checks = []
        all_valid = True

        for task in tasks:
            is_valid = task.status in [TaskStatus.FOR_RELEASE.value, TaskStatus.IN_RELEASE.value]
            problem = None if is_valid else f"Task is in '{task.status}' status, should be 'For Release' or 'In Release'"
            
            tag_names = [tag.name for tag in task.tags]
            
            task_check = ReleaseTaskCheck(
                task_id=task.id,
                title=task.title,
                status=task.status,
                author=task.author,
                developer=task.developer,
                tags=tag_names,
                problem=problem
            )
            
            task_checks.append(task_check)
            
            if not is_valid:
                all_valid = False

        return task_checks, all_valid

    def check_task_dependencies(self, release_task_id: int) -> Tuple[List[ReleaseTaskDependencyCheck], bool]:
        """Check if all task dependencies are included in the release."""
        release_task = self.db.query(Task).filter(Task.id == release_task_id).first()
        if not release_task:
            return [], False

        # Get all tasks that are dependencies of the release task
        release_tasks = set()
        for task in release_task.dependencies:
            release_tasks.add(task.id)

        dependency_checks = []
        all_valid = True

        for task in release_task.dependencies:
            for dep_task in task.dependencies:
                in_release = dep_task.id in release_tasks
                
                check = ReleaseTaskDependencyCheck(
                    task_id=task.id,
                    title=task.title,
                    dependency_id=dep_task.id,
                    dependency_title=dep_task.title,
                    in_release=in_release
                )
                
                dependency_checks.append(check)
                
                if not in_release:
                    all_valid = False

        return dependency_checks, all_valid

    def create_release_branch(
        self, 
        project_id: int, 
        source_branch_name: str, 
        release_name: str
    ) -> ReleaseBranchResponse:
        """Create a release branch from the source branch."""
        project = self.db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return ReleaseBranchResponse(
                success=False,
                message="Project not found"
            )

        # Check if the branch already exists
        branch = self.db.query(Branch).filter(
            Branch.project_id == project_id,
            Branch.name == release_name,
            Branch.is_release_branch == True
        ).first()
        
        if branch:
            return ReleaseBranchResponse(
                success=True,
                message="Release branch already exists",
                branch_id=branch.id,
                branch_name=branch.name
            )

        # Get the source branch
        source_branch = self.db.query(Branch).filter(
            Branch.project_id == project_id,
            Branch.name == source_branch_name
        ).first()
        
        if not source_branch:
            return ReleaseBranchResponse(
                success=False,
                message=f"Source branch '{source_branch_name}' not found"
            )

        # Create the branch in the database
        new_branch = Branch(
            name=release_name,
            project_id=project_id,
            is_release_branch=True
        )
        
        self.db.add(new_branch)
        self.db.commit()
        self.db.refresh(new_branch)

        return ReleaseBranchResponse(
            success=True,
            message="Release branch created successfully",
            branch_id=new_branch.id,
            branch_name=new_branch.name
        )

    def check_project_dependencies(self, release_task_id: int) -> Tuple[List[Dict[str, Any]], bool]:
        """Check if tasks have dependencies on other projects."""
        release_task = self.db.query(Task).filter(Task.id == release_task_id).first()
        if not release_task:
            return [], False

        # Упрощенная реализация, возвращаем пустой список и True (нет внешних зависимостей)
        return [], True

    def assemble_release(
        self, 
        release_data: ReleaseCreate
    ) -> ReleaseAssemblyResponse:
        """Assemble a new release by checking tasks and creating branches and MRs."""
        # 1. Check if all tasks have correct statuses
        task_checks, all_tasks_valid = self.check_task_statuses(release_data.release_task_id)
        
        # 2. Check task dependencies
        dependency_checks, all_deps_valid = self.check_task_dependencies(release_data.release_task_id)
        
        # 3. Check project dependencies
        project_dep_checks, no_ext_deps = self.check_project_dependencies(release_data.release_task_id)

        # Prepare checks for the response
        checks = []
        
        # Task status check
        task_status_check = {
            "type": "task_status",
            "status": CheckStatusEnum.SUCCESS if all_tasks_valid else CheckStatusEnum.ERROR,
            "message": "All tasks have correct status" if all_tasks_valid else "Some tasks have incorrect status",
            "data": [check.dict() for check in task_checks]
        }
        checks.append(task_status_check)
        
        # Task dependency check
        task_dep_check = {
            "type": "task_dependencies",
            "status": CheckStatusEnum.SUCCESS if all_deps_valid else CheckStatusEnum.WARNING,
            "message": "All dependencies included in release" if all_deps_valid else "Some dependencies are missing from release",
            "data": [check.dict() for check in dependency_checks]
        }
        checks.append(task_dep_check)
        
        # Project dependency check
        project_dep_check = {
            "type": "project_dependencies",
            "status": CheckStatusEnum.SUCCESS if no_ext_deps else CheckStatusEnum.WARNING,
            "message": "No external dependencies" if no_ext_deps else "Has dependencies on other projects",
            "data": project_dep_checks
        }
        checks.append(project_dep_check)
        
        # If there are critical errors, return without creating the release
        if not all_tasks_valid:
            return ReleaseAssemblyResponse(
                success=False,
                message="Release assembly failed: Some tasks have incorrect status",
                checks=checks
            )

        # 4. Create release branch if not exists
        release_task = self.db.query(Task).filter(Task.id == release_data.release_task_id).first()
        if not release_task:
            return ReleaseAssemblyResponse(
                success=False,
                message="Release task not found",
                checks=checks
            )
            
        project = self.db.query(Project).filter(Project.id == release_data.project_id).first()
        if not project:
            return ReleaseAssemblyResponse(
                success=False,
                message="Project not found",
                checks=checks
            )
            
        # Release branch name could be derived from release task or provided
        branch_name = f"release/{release_data.name}"
        
        branch_response = self.create_release_branch(
            project_id=release_data.project_id, 
            source_branch_name=release_data.source_branch_name, 
            release_name=branch_name
        )
        
        if not branch_response.success:
            return ReleaseAssemblyResponse(
                success=False,
                message=f"Failed to create release branch: {branch_response.message}",
                checks=checks
            )
            
        # 5. Create a new release record
        new_release = Release(
            name=release_data.name,
            description=release_data.description,
            status=ReleaseStatus.DRAFT,
            project_id=release_data.project_id,
            branch_id=branch_response.branch_id,
            source_branch_id=release_data.source_branch_id,
            release_task_id=release_data.release_task_id,
            skip_pipeline=release_data.skip_pipeline
        )
        
        self.db.add(new_release)
        self.db.flush()  # Get the ID without committing
        
        # 6. Create release checks
        for check_data in checks:
            release_check = ReleaseCheck(
                release_id=new_release.id,
                check_type=check_data["type"],
                status=check_data["status"],
                message=check_data["message"],
                details=json.dumps(check_data["data"])
            )
            self.db.add(release_check)
            
        # 7. Add tasks to the release
        for task in release_task.dependencies:
            task.release_id = new_release.id
            
        # Commit all changes
        self.db.commit()
        self.db.refresh(new_release)
        
        return ReleaseAssemblyResponse(
            success=True,
            message="Release assembled successfully",
            release_id=new_release.id,
            checks=checks
        )

    def add_task_to_release(
        self, 
        release_id: int, 
        task_id: int
    ) -> Dict[str, Any]:
        """Add a task to an existing release."""
        release = self.db.query(Release).filter(Release.id == release_id).first()
        if not release:
            return {"success": False, "message": "Release not found"}
            
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return {"success": False, "message": "Task not found"}
            
        project = self.db.query(Project).filter(Project.id == release.project_id).first()
        if not project:
            return {"success": False, "message": "Project not found"}
            
        # Check if task already in release
        if task.release_id == release_id:
            return {"success": True, "message": "Task is already in the release"}
            
        # Check task status
        if task.status not in [TaskStatus.FOR_RELEASE.value, TaskStatus.IN_RELEASE.value]:
            return {
                "success": False, 
                "message": f"Task status is '{task.status}', should be 'For Release' or 'In Release'"
            }
            
        # Add task to release
        task.release_id = release_id
        
        self.db.commit()
        return {"success": True, "message": "Task added to release successfully"}

    def get_release_commits(self, release_id: int) -> List[Dict[str, Any]]:
        """Get all commits that are part of a release."""
        # TODO возвращаем заглушку
        return []

    def compare_tasks_with_commits(self, release_id: int) -> Dict[str, Any]:
        """Compare tasks in the release with commits to ensure all are included."""
        release = self.db.query(Release).filter(Release.id == release_id).first()
        if not release:
            return {"success": False, "message": "Release not found"}
            
        # Получаем задачи релиза
        release_tasks = self.db.query(Task).filter(Task.release_id == release_id).all()
        
        # TODO возвращаем упрощенный ответ
        return {
            "success": True,
            "all_match": True,
            "matched_tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "status": task.status
                }
                for task in release_tasks
            ],
            "unmatched_tasks": [],
            "unmatched_commits": []
        } 