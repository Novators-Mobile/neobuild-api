from typing import List, Optional, Dict, Any
import requests
from app.core.config import settings

class GitLabService:
    def __init__(self):
        self.base_url = settings.GITLAB_URL
        self.token = settings.GITLAB_TOKEN
        self.headers = {
            "PRIVATE-TOKEN": self.token,
            "Content-Type": "application/json"
        }

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project details from GitLab"""
        response = requests.get(
            f"{self.base_url}/api/v4/projects/{project_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_branches(self, project_id: str) -> List[Dict[str, Any]]:
        """Get all branches for a project"""
        response = requests.get(
            f"{self.base_url}/api/v4/projects/{project_id}/repository/branches",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def create_branch(self, project_id: str, branch_name: str, ref: str) -> Dict[str, Any]:
        """Create a new branch in the project"""
        data = {
            "branch": branch_name,
            "ref": ref
        }
        response = requests.post(
            f"{self.base_url}/api/v4/projects/{project_id}/repository/branches",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def create_merge_request(
        self,
        project_id: str,
        source_branch: str,
        target_branch: str,
        title: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a merge request"""
        data = {
            "source_branch": source_branch,
            "target_branch": target_branch,
            "title": title,
            "description": description
        }
        response = requests.post(
            f"{self.base_url}/api/v4/projects/{project_id}/merge_requests",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def get_merge_requests(self, project_id: str, state: str = "opened") -> List[Dict[str, Any]]:
        """Get merge requests for a project"""
        params = {"state": state}
        response = requests.get(
            f"{self.base_url}/api/v4/projects/{project_id}/merge_requests",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def accept_merge_request(self, project_id: str, merge_request_iid: int) -> Dict[str, Any]:
        """Accept a merge request"""
        response = requests.put(
            f"{self.base_url}/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/merge",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json() 