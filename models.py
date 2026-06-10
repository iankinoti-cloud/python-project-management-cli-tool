from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class User:
    id: int
    name: str
    email: str
    project_ids: List[int] = field(default_factory=list)

    def add_project(self, project_id: int) -> None:
        if project_id not in self.project_ids:
            self.project_ids.append(project_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "project_ids": self.project_ids,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "User":
        return User(
            id=int(data["id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            project_ids=list(data.get("project_ids", [])),
        )


@dataclass
class Project:
    id: int
    name: str
    owner_user_id: int
    task_ids: List[int] = field(default_factory=list)

    def add_task(self, task_id: int) -> None:
        if task_id not in self.task_ids:
            self.task_ids.append(task_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "owner_user_id": self.owner_user_id,
            "task_ids": self.task_ids,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Project":
        return Project(
            id=int(data["id"]),
            name=str(data["name"]),
            owner_user_id=int(data["owner_user_id"]),
            task_ids=list(data.get("task_ids", [])),
        )


@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str
    project_id: int
    contributor_ids: List[int] = field(default_factory=list)

    def complete(self) -> None:
        self.status = "complete"

    def add_contributor(self, user_id: int) -> None:
        if user_id not in self.contributor_ids:
            self.contributor_ids.append(user_id)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "project_id": self.project_id,
            "contributor_ids": self.contributor_ids,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        return Task(
            id=int(data["id"]),
            title=str(data["title"]),
            description=str(data.get("description", "")),
            status=str(data.get("status", "open")),
            project_id=int(data["project_id"]),
            contributor_ids=list(data.get("contributor_ids", [])),
        )
