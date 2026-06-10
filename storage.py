import json
import os
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from models import Project, Task, User


class DataStoreError(Exception):
    pass


class DataStore:
    def __init__(self, path: Optional[str] = None):
        self.filepath = Path(path or Path(__file__).resolve().parent / "data.json")
        self._data = self._load_data()

    def _load_data(self) -> Dict[str, object]:
        if self.filepath.exists():
            try:
                with self.filepath.open("r", encoding="utf-8") as source:
                    data = json.load(source)
            except (json.JSONDecodeError, OSError) as exc:
                raise DataStoreError(f"Unable to load {self.filepath}: {exc}")

            return {
                "users": {int(k): User.from_dict(v) for k, v in data.get("users", {}).items()},
                "projects": {int(k): Project.from_dict(v) for k, v in data.get("projects", {}).items()},
                "tasks": {int(k): Task.from_dict(v) for k, v in data.get("tasks", {}).items()},
                "next_ids": {
                    "user": int(data.get("next_ids", {}).get("user", 1)),
                    "project": int(data.get("next_ids", {}).get("project", 1)),
                    "task": int(data.get("next_ids", {}).get("task", 1)),
                },
            }
        return {
            "users": {},
            "projects": {},
            "tasks": {},
            "next_ids": {"user": 1, "project": 1, "task": 1},
        }

    def save(self) -> None:
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "users": {str(uid): user.to_dict() for uid, user in self._data["users"].items()},
            "projects": {str(pid): project.to_dict() for pid, project in self._data["projects"].items()},
            "tasks": {str(tid): task.to_dict() for tid, task in self._data["tasks"].items()},
            "next_ids": self._data["next_ids"],
        }
        try:
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=self.filepath.parent) as handle:
                json.dump(data, handle, indent=2)
                temp_path = Path(handle.name)
            os.replace(temp_path, self.filepath)
        except OSError as exc:
            raise DataStoreError(f"Unable to save {self.filepath}: {exc}")

    def _next_id(self, kind: str) -> int:
        next_id = self._data["next_ids"][kind]
        self._data["next_ids"][kind] = next_id + 1
        return next_id

    def add_user(self, name: str, email: str) -> User:
        user_id = self._next_id("user")
        user = User(id=user_id, name=name, email=email)
        self._data["users"][user_id] = user
        self.save()
        return user

    def list_users(self) -> List[User]:
        return sorted(self._data["users"].values(), key=lambda u: u.id)

    def get_user(self, user_id: int) -> User:
        user = self._data["users"].get(user_id)
        if not user:
            raise KeyError(f"User {user_id} not found")
        return user

    def add_project(self, user_id: int, name: str) -> Project:
        owner = self.get_user(user_id)
        project_id = self._next_id("project")
        project = Project(id=project_id, name=name, owner_user_id=owner.id)
        self._data["projects"][project_id] = project
        owner.add_project(project_id)
        self.save()
        return project

    def list_projects(self, user_id: Optional[int] = None) -> List[Project]:
        projects = list(self._data["projects"].values())
        if user_id is not None:
            self.get_user(user_id)
            projects = [project for project in projects if project.owner_user_id == user_id]
        return sorted(projects, key=lambda p: p.id)

    def get_project(self, project_id: int) -> Project:
        project = self._data["projects"].get(project_id)
        if not project:
            raise KeyError(f"Project {project_id} not found")
        return project

    def add_task(self, project_id: int, title: str, description: str, contributor_ids: Optional[List[int]] = None) -> Task:
        project = self.get_project(project_id)
        if contributor_ids is None:
            contributor_ids = []
        valid_contributors = []
        for user_id in contributor_ids:
            if user_id not in self._data["users"]:
                raise KeyError(f"Contributor {user_id} not found")
            if user_id not in valid_contributors:
                valid_contributors.append(user_id)
        task_id = self._next_id("task")
        task = Task(
            id=task_id,
            title=title,
            description=description,
            status="open",
            project_id=project.id,
            contributor_ids=valid_contributors,
        )
        self._data["tasks"][task_id] = task
        project.add_task(task_id)
        self.save()
        return task

    def list_tasks(self, project_id: Optional[int] = None) -> List[Task]:
        tasks = list(self._data["tasks"].values())
        if project_id is not None:
            self.get_project(project_id)
            tasks = [task for task in tasks if task.project_id == project_id]
        return sorted(tasks, key=lambda t: t.id)

    def get_task(self, task_id: int) -> Task:
        task = self._data["tasks"].get(task_id)
        if not task:
            raise KeyError(f"Task {task_id} not found")
        return task

    def complete_task(self, task_id: int) -> Task:
        task = self.get_task(task_id)
        task.complete()
        self.save()
        return task

    def assign_contributor(self, task_id: int, user_id: int) -> Task:
        task = self.get_task(task_id)
        user = self.get_user(user_id)
        task.add_contributor(user.id)
        self.save()
        return task
