# models/user.py

class User:
    """Represents a user in the project management system."""

    user_counter = 1  # class attribute for generating unique IDs

    def __init__(self, name, email):
        self.id = User.user_counter
        User.user_counter += 1
        self.name = name
        self.email = email
        self.projects = []  # one-to-many: a user can have many projects

    def add_project(self, project):
        """Associate a Project instance with this user."""
        self.projects.append(project)

    def list_projects(self):
        """Return the titles of all projects owned by this user."""
        return [project.title for project in self.projects]

    def __repr__(self):
        return f"<User {self.id}: {self.name} ({self.email})>"
