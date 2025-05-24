from typing import List, Optional, Dict, Any
import requests
from app.core.config import settings

class YouTrackService:
    def __init__(self):
        self.base_url = settings.YOUTRACK_URL
        self.token = settings.YOUTRACK_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get_issue(self, issue_id: str) -> Dict[str, Any]:
        """Get issue details from YouTrack"""
        response = requests.get(
            f"{self.base_url}/api/issues/{issue_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def create_issue(
        self,
        project_id: str,
        summary: str,
        description: Optional[str] = None,
        **fields
    ) -> Dict[str, Any]:
        """Create a new issue in YouTrack"""
        data = {
            "project": {"id": project_id},
            "summary": summary,
            "description": description,
            **fields
        }
        response = requests.post(
            f"{self.base_url}/api/issues",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def update_issue(self, issue_id: str, **fields) -> Dict[str, Any]:
        """Update an existing issue"""
        response = requests.post(
            f"{self.base_url}/api/issues/{issue_id}",
            headers=self.headers,
            json=fields
        )
        response.raise_for_status()
        return response.json()

    def get_issues(
        self,
        project_id: str,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Get issues for a project with optional filtering"""
        params = {
            "query": f"project: {project_id} {query or ''}",
            "fields": ",".join(fields) if fields else None
        }
        response = requests.get(
            f"{self.base_url}/api/issues",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()

    def add_comment(self, issue_id: str, text: str) -> Dict[str, Any]:
        """Add a comment to an issue"""
        data = {"text": text}
        response = requests.post(
            f"{self.base_url}/api/issues/{issue_id}/comments",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def get_issue_links(self, issue_id: str) -> List[Dict[str, Any]]:
        """Get all links for an issue"""
        response = requests.get(
            f"{self.base_url}/api/issues/{issue_id}/links",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def create_issue_link(
        self,
        issue_id: str,
        linked_issue_id: str,
        link_type: str
    ) -> Dict[str, Any]:
        """Create a link between two issues"""
        data = {
            "issueId": linked_issue_id,
            "type": link_type
        }
        response = requests.post(
            f"{self.base_url}/api/issues/{issue_id}/links",
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json() 