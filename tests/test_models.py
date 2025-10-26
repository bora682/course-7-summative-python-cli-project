from models.user import User
from models.project import Project
from models.task import Task

def test_user_creation():
    user = User("Alice", "alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"

def test_project_creation():
    user = User("Bob", "bob@example.com")
    # Correct arg order: title, owner, description, due_date
    project = Project("CLI Tool", owner=user, description="Build project CLI", due_date="2025-11-15")
    assert project.title == "CLI Tool"
    assert project.description == "Build project CLI"
    assert project.owner == user

def test_task_creation():
    # Owner can be None; order is title, owner, description, due_date in Project
    project = Project("CLI Tool", owner=None, description="Test tasks", due_date="2025-11-15")
    task = Task("Write tests", project=project, status="todo")
    assert task.title == "Write tests"
    assert task.status == "todo"
    assert task in project.tasks
