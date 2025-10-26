from models.user import User
from models.project import Project
from models.task import Task
from utils.file_io import save_all, load_all

def test_save_and_load(tmp_path):
    # Build real objects (what save_all expects)
    u = User("Alice", "alice@example.com")
    p = Project("Capstone", owner=u, description="Finish SPA", due_date="2025-11-15")
    t = Task("Write README", project=p, status="todo")
    t.assign(u)

    storage = tmp_path / "storage.json"

    # Save
    save_all([u], path=str(storage))
    assert storage.exists() and storage.stat().st_size > 0

    # Load
    users_loaded = load_all(path=str(storage))
    assert len(users_loaded) == 1
    u2 = users_loaded[0]
    assert u2.name == "Alice"
    assert len(u2.projects) == 1
    p2 = u2.projects[0]
    assert p2.title == "Capstone"
    assert len(p2.tasks) == 1
    t2 = p2.tasks[0]
    assert t2.title == "Write README"
    assert any(c.email == "alice@example.com" for c in t2.contributors)
