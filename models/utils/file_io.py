# utils/file_io.py
import json
import os
from typing import List, Dict, Any, Tuple
from models.user import User
from models.project import Project
from models.task import Task

STORAGE_PATH = os.path.join("data", "storage.json")


def _collect_state(users: List[User]) -> Dict[str, Any]:
    """
    Walk the object graph (users -> projects -> tasks) and produce
    a JSON-serializable dict with de-duplicated projects and tasks.
    """
    users_out = []
    projects_out = {}
    tasks_out = {}

    for u in users:
        users_out.append({
            "id": u.id,
            "name": u.name,
            "email": u.email,
        })
        for p in u.projects:
            if p.id not in projects_out:
                projects_out[p.id] = {
                    "id": p.id,
                    "title": p.title,
                    "description": p.description,
                    "due_date": p.due_date,
                    "owner_id": u.id,
                }
            for t in p.tasks:
                if t.id not in tasks_out:
                    tasks_out[t.id] = {
                        "id": t.id,
                        "title": t.title,
                        "status": t.status,
                        "project_id": p.id,
                        "contributor_ids": [cu.id for cu in t.contributors],
                    }

    return {
        "users": users_out,
        "projects": list(projects_out.values()),
        "tasks": list(tasks_out.values()),
    }


def save_all(users: List[User], path: str = STORAGE_PATH) -> None:
    """
    Persist the entire in-memory state to JSON. Writes atomically
    (via a temp file + replace) to avoid corrupting storage.json.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = _collect_state(users)
    tmp_path = f"{path}.tmp"

    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    # optional backup
    if os.path.exists(path):
        try:
            os.replace(path, f"{path}.bak")
        except Exception:
            pass

    os.replace(tmp_path, path)


def load_all(path: str = STORAGE_PATH) -> List[User]:
    """
    Load JSON, rebuild User/Project/Task objects, repair relationships,
    and fix the class ID counters. Returns the list of User objects.
    """
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # --- 1) Rebuild Users ---
    users_by_id: Dict[int, User] = {}
    max_user_id = 0
    for u in data.get("users", []):
        user = User(u["name"], u["email"])
        user.id = int(u["id"])
        users_by_id[user.id] = user
        if user.id > max_user_id:
            max_user_id = user.id

    # --- 2) Rebuild Projects (with owner) ---
    projects_by_id: Dict[int, Project] = {}
    max_project_id = 0
    for p in data.get("projects", []):
        owner = users_by_id.get(int(p["owner_id"]))
        proj = Project(
            title=p["title"],
            owner=owner,
            description=p.get("description"),
            due_date=p.get("due_date"),
        )
        proj.id = int(p["id"])
        projects_by_id[proj.id] = proj
        if proj.id > max_project_id:
            max_project_id = proj.id

    # --- 3) Rebuild Tasks (with project + contributors) ---
    max_task_id = 0
    for t in data.get("tasks", []):
        project = projects_by_id.get(int(t["project_id"]))
        task = Task(
            title=t["title"],
            project=project,
            status=t.get("status", "todo"),
        )
        task.id = int(t["id"])
        # contributors
        for uid in t.get("contributor_ids", []):
            u = users_by_id.get(int(uid))
            if u:
                task.assign(u)
        if task.id > max_task_id:
            max_task_id = task.id

    # --- 4) Fix ID counters so future creations get unique IDs ---
    User.user_counter = max_user_id + 1 if max_user_id else 1
    Project.project_counter = max_project_id + 1 if max_project_id else 1
    Task.task_counter = max_task_id + 1 if max_task_id else 1

    # Return users in a stable order
    return [users_by_id[k] for k in sorted(users_by_id.keys())]
