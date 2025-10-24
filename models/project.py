# models/project.py

class Project:
    """Represents a project owned by a user and containing tasks."""

    project_counter = 1

    def __init__(self, title, owner, description=None, due_date=None):
        """
        owner: a User instance (from models.user import User)
        """
        self.id = Project.project_counter
        Project.project_counter += 1

        self.title = title
        self.description = description
        self.due_date = due_date  
        self.owner = owner       
        self.tasks = []           

        # maintain back-reference on the owner
        if self.owner is not None:
            self.owner.add_project(self)

    def add_task(self, task):
        """Associate a Task instance with this project."""
        self.tasks.append(task)

    def list_tasks(self):
        """Return the titles of all tasks for this project."""
        return [t.title for t in self.tasks]

    def __repr__(self):
        return f"<Project {self.id}: {self.title} (owner={self.owner.name if self.owner else 'None'})>"
