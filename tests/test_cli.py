# tests/test_cli.py
import subprocess
import json
import os

DATA_PATH = "data/storage.json"

def run_cli(args):
    """Helper to run CLI commands."""
    result = subprocess.run(
        ["python3", "main.py"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def test_add_user_and_list():
    # Clean up any previous data
    if os.path.exists(DATA_PATH):
        os.remove(DATA_PATH)

    # Add user
    output = run_cli(["add-user", "--name", "Alice", "--email", "alice@example.com"])
    assert "Created user" in output

    # List users
    list_output = run_cli(["list-users"])
    assert "Alice" in list_output
    assert "alice@example.com" in list_output

def test_add_project_and_task():
    # Add project
    output = run_cli([
        "add-project",
        "--user", "alice@example.com",
        "--title", "Capstone",
        "--description", "Finish SPA",
        "--due-date", "2025-11-15"
    ])
    assert "Created project" in output

    # Add task
    task_output = run_cli(["add-task", "--project", "Capstone", "--title", "Write README"])
    assert "Created task" in task_output

def test_complete_task_and_list():
    # Complete the first task
    complete_output = run_cli(["complete-task", "--id", "1"])
    assert "Completed task" in complete_output

    # Verify list shows [done]
    list_output = run_cli(["list-tasks", "--project", "Capstone"])
    assert "[done]" in list_output
