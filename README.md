# Python Project Management CLI Tool

## Overview
A command-line tool that lets users manage **projects, tasks, and team members.**
Built in Python using OOP principles, JSON persistence, and argparse for the CLI.

---

## Main Features
- Add and list users, projects, and tasks
- Mark tasks as complete
- Save and load data using JSON
- Organized with folders: `models/`, `utils/`, `data/`, and `tests/`
- All pytest tests pass

---

## Example Commands

**Run these in your terminal:**

```bash
python3 main.py add-user --name "Alice" --email alice@example.com
python3 main.py add-project --user alice@example.com --title "Capstone"
python3 main.py add-task --project "Capstone" --title "Write README"
python3 main.py complete-task --id 1
python3 main.py list-tasks
```

---

## Testing
**Run all tests:**

```bash
pytest -v
```

All 7 tests pass successfully

---

## Project Structure
main.py
models/
utils/
data/
tests/
requirements.txt

---

## Author
**Deborah Im**
Flatiron School - Software Engineering Program 
Github: [bora682](https://github.com/bora682)