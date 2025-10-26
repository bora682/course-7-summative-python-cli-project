# main.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse
from utils.file_io import load_all, save_all
from models.user import User
from models.project import Project
from models.task import Task


# ---------- helpers ----------
def find_user(users, name_or_email):
    for u in users:
        if u.name == name_or_email or u.email == name_or_email:
            return u
    return None

def find_project(users, title):
    for u in users:
        for p in u.projects:
            if p.title == title:
                return p
    return None

def list_all_projects(users):
    out = []
    for u in users:
        for p in u.projects:
            out.append(p)
    return out

def find_task_by_id(users, task_id: int):
    for p in list_all_projects(users):
        for t in p.tasks:
            if t.id == task_id:
                return t
    return None


# ---------- command handlers ----------
def cmd_add_user(args, users):
    # basic validation
    if not args.name or not args.email:
        print("Error: --name and --email are required.", file=sys.stderr)
        return 1
    # prevent duplicate by email
    if find_user(users, args.email):
        print(f"Error: user with email {args.email} already exists.", file=sys.stderr)
        return 1

    u = User(args.name, args.email)
    users.append(u)
    save_all(users)
    print(f"Created user: {u}")
    return 0

def cmd_list_users(args, users):
    if not users:
        print("No users found.")
        return 0
    for u in users:
        print(f"{u.id}\t{u.name}\t{u.email}")
    return 0

def cmd_add_project(args, users):
    owner = find_user(users, args.user)
    if not owner:
        print(f"Error: user '{args.user}' not found by name or email.", file=sys.stderr)
        return 1
    if find_project(users, args.title):
        print(f"Error: project with title '{args.title}' already exists.", file=sys.stderr)
        return 1

    p = Project(
        title=args.title,
        owner=owner,
        description=args.description,
        due_date=args.due_date,
    )
    save_all(users)
    print(f"Created project: {p}")
    return 0

def cmd_list_projects(args, users):
    if args.user:
        owner = find_user(users, args.user)
        if not owner:
            print(f"Error: user '{args.user}' not found.", file=sys.stderr)
            return 1
        if not owner.projects:
            print(f"No projects for {owner.name}.")
            return 0
        for p in owner.projects:
            print(f"{p.id}\t{p.title}\towner={owner.name}\tdue={p.due_date or '-'}")
        return 0

    # list all projects
    allp = list_all_projects(users)
    if not allp:
        print("No projects found.")
        return 0
    for p in allp:
        print(f"{p.id}\t{p.title}\towner={p.owner.name}\tdue={p.due_date or '-'}")
    return 0

def cmd_add_task(args, users):
    project = find_project(users, args.project)
    if not project:
        print(f"Error: project '{args.project}' not found by title.", file=sys.stderr)
        return 1

    t = Task(args.title, project=project, status="todo")
    # optional assignment
    if args.assign:
        # allow assign by name or email
        user = find_user(users, args.assign)
        if not user:
            print(f"Warning: contributor '{args.assign}' not found; task created unassigned.", file=sys.stderr)
        else:
            t.assign(user)

    save_all(users)
    print(f"Created task: {t}")
    return 0

def cmd_list_tasks(args, users):
    project = find_project(users, args.project) if args.project else None
    tasks_to_show = []
    if project:
        tasks_to_show = project.tasks
    else:
        # all tasks across all projects
        for p in list_all_projects(users):
            tasks_to_show.extend(p.tasks)

    if not tasks_to_show:
        print("No tasks found.")
        return 0

    for t in tasks_to_show:
        proj_title = t.project.title if t.project else "-"
        contributors = ", ".join([u.name for u in t.contributors]) or "-"
        print(f"{t.id}\t{t.title}\t[{t.status}]\tproj={proj_title}\tcontributors={contributors}")
    return 0

def cmd_complete_task(args, users):
    try:
        task_id = int(args.id)
    except ValueError:
        print("Error: --id must be an integer.", file=sys.stderr)
        return 1

    t = find_task_by_id(users, task_id)
    if not t:
        print(f"Error: task id {task_id} not found.", file=sys.stderr)
        return 1

    t.complete()
    save_all(users)
    print(f"Completed task: {t}")
    return 0


# ---------- argparse wiring ----------
def build_parser():
    parser = argparse.ArgumentParser(
        description="Project Management CLI (users, projects, tasks)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # add-user
    p_add_user = sub.add_parser("add-user", help="Create a new user")
    p_add_user.add_argument("--name", required=True)
    p_add_user.add_argument("--email", required=True)
    p_add_user.set_defaults(func=cmd_add_user)

    # list-users
    p_list_users = sub.add_parser("list-users", help="List all users")
    p_list_users.set_defaults(func=cmd_list_users)

    # add-project
    p_add_proj = sub.add_parser("add-project", help="Create a project for a user")
    p_add_proj.add_argument("--user", required=True, help="Owner name or email")
    p_add_proj.add_argument("--title", required=True)
    p_add_proj.add_argument("--description")
    p_add_proj.add_argument("--due-date")
    p_add_proj.set_defaults(func=cmd_add_project)

    # list-projects
    p_list_proj = sub.add_parser("list-projects", help="List projects (optionally for a specific user)")
    p_list_proj.add_argument("--user", help="Owner name or email")
    p_list_proj.set_defaults(func=cmd_list_projects)

    # add-task
    p_add_task = sub.add_parser("add-task", help="Create a task in a project")
    p_add_task.add_argument("--project", required=True, help="Project title")
    p_add_task.add_argument("--title", required=True)
    p_add_task.add_argument("--assign", help="Contributor name or email (optional)")
    p_add_task.set_defaults(func=cmd_add_task)

    # list-tasks
    p_list_tasks = sub.add_parser("list-tasks", help="List tasks (optionally by project)")
    p_list_tasks.add_argument("--project", help="Project title")
    p_list_tasks.set_defaults(func=cmd_list_tasks)

    # complete-task
    p_complete = sub.add_parser("complete-task", help="Mark a task complete by id")
    p_complete.add_argument("--id", required=True, help="Task ID (integer)")
    p_complete.set_defaults(func=cmd_complete_task)

    return parser


def main(argv=None):
    # 1) load persisted data
    users = load_all()

    # 2) parse args & dispatch
    parser = build_parser()
    args = parser.parse_args(argv)

    # 3) run handler
    rc = args.func(args, users)

    # Handlers save on success, but you could add centralized save here if desired.
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
