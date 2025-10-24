# models/task.py

class Task:
    """Represents a task within a project, optionally with contributors."""

    task_counter = 1

    def __init__(self, title, project, status="todo"):
        """
        title: str
        project: a Project instance (from models.project import Project)
        status: "todo" | "in_progress" | "done"
        """
        self.id = Task.task_counter
        Task.task_counter += 1

        self.title = title
        self.status = status
        self.project = project
        self.contributors = []  # list of User instances

        # keep project -> tasks backlink in sync
        if self.project is not None:
            self.project.add_task(self)

    def assign(self, user):
        """Add a User as a contributor if not already present."""
        if user not in self.contributors:
            self.contributors.append(user)

    def unassign(self, user):
        """Remove a User from contributors if present."""
        if user in self.contributors:
            self.contributors.remove(user)

    def complete(self):
        """Mark the task as done."""
        self.status = "done"

    def __repr__(self):
        names = [u.name for u in self.contributors]
        return f"<Task {self.id}: {self.title} [{self.status}] contributors={names}>"
