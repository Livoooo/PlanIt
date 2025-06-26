"""
Textual modal dialogs for PlanIt TUI
"""

from textual.screen import ModalScreen
from textual.containers import Container, Horizontal
from textual.widgets import Button, Static, Label, Input
from textual.app import ComposeResult
from planit.core.database import TaskManager

# Instance globale pour les modals
planner = TaskManager()


class AddTaskModal(ModalScreen):
    """Modal for adding a new task"""
    
    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static("➕ Add New Task", classes="title")
            yield Label("Task Title:")
            yield Input(placeholder="Enter task title...", id="title_input")
            yield Label("Duration (hours):")
            yield Input(placeholder="1", id="duration_input")
            
            with Horizontal():
                yield Button("Add Task", variant="primary", id="confirm")
                yield Button("Back", variant="default", id="back")
                yield Button("Cancel", variant="default", id="cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            title_input = self.query_one("#title_input", Input)
            duration_input = self.query_one("#duration_input", Input)
            
            title = title_input.value.strip()
            try:
                duration = int(duration_input.value)
                if title and duration > 0:
                    planner.add_task(title, duration)
                    self.app.update_content(f"✅ Task '{title}' added successfully!")
                    self.dismiss()
                else:
                    self.app.update_content("❌ Please enter valid title and duration")
            except ValueError:
                self.app.update_content("❌ Duration must be a number")
        elif event.button.id == "back":
            self.app.action_go_back()
            self.dismiss()
        else:
            self.dismiss()


class DeleteTaskModal(ModalScreen):
    """Modal for deleting a task"""
    
    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static("🗑️ Delete Task", classes="title")
            yield Label("Task ID:")
            yield Input(placeholder="Enter task ID...", id="task_id_input")
            
            with Horizontal():
                yield Button("Delete", variant="error", id="confirm")
                yield Button("Back", variant="default", id="back")
                yield Button("Cancel", variant="default", id="cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            task_id_input = self.query_one("#task_id_input", Input)
            
            try:
                task_id = int(task_id_input.value)
                planner.delete_task(task_id)
                self.app.update_content(f"🗑️ Task {task_id} deleted!")
                self.dismiss()
            except ValueError:
                self.app.update_content("❌ Task ID must be a number")
        elif event.button.id == "back":
            self.app.action_go_back()
            self.dismiss()
        else:
            self.dismiss()


class AddProjectModal(ModalScreen):
    """Modal for adding a new project"""
    
    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static("📊 Add New Project", classes="title")
            yield Label("Project Name:")
            yield Input(placeholder="Enter project name...", id="name_input")
            yield Label("Start Date (MM/DD):")
            yield Input(placeholder="06/01", id="start_input")
            yield Label("End Date (MM/DD):")
            yield Input(placeholder="08/31", id="end_input")
            yield Label("Description (optional):")
            yield Input(placeholder="Project description...", id="desc_input")
            
            with Horizontal():
                yield Button("Add Project", variant="primary", id="confirm")
                yield Button("Back", variant="default", id="back")
                yield Button("Cancel", variant="default", id="cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            name_input = self.query_one("#name_input", Input)
            start_input = self.query_one("#start_input", Input)
            end_input = self.query_one("#end_input", Input)
            desc_input = self.query_one("#desc_input", Input)
            
            name = name_input.value.strip()
            start_date = start_input.value.strip()
            end_date = end_input.value.strip()
            description = desc_input.value.strip()
            
            # Validate input
            if not name:
                self.app.update_content("❌ Please enter a project name")
                return
            
            if not start_date:
                self.app.update_content("❌ Please enter a start date")
                return
                
            if not end_date:
                self.app.update_content("❌ Please enter an end date")
                return
            
            # Validate dates
            try:
                for date_str, label in [(start_date, "start"), (end_date, "end")]:
                    if '/' not in date_str:
                        raise ValueError(f"Invalid {label} date format")
                    month, day = date_str.split('/')
                    month = int(month)
                    day = int(day)
                    if month < 1 or month > 12 or day < 1 or day > 31:
                        raise ValueError(f"Invalid {label} date values")
                
                # CRITICAL: Call add_project, NOT add_task
                planner.add_project(name, start_date, end_date, description)
                self.app.update_content(f"📊 Project '{name}' added successfully! Use 'timeline' to see it.")
                self.dismiss()
                
            except (ValueError, IndexError) as e:
                self.app.update_content("❌ Invalid date format. Use MM/DD (e.g., 06/15)")
        elif event.button.id == "back":
            self.app.action_go_back()
            self.dismiss()
        else:
            self.dismiss()


class MarkDoneModal(ModalScreen):
    """Modal for marking task as done"""
    
    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static("✅ Mark Task as Done", classes="title")
            yield Label("Task ID:")
            yield Input(placeholder="Enter task ID...", id="task_id_input")
            
            with Horizontal():
                yield Button("Mark Done", variant="success", id="confirm")
                yield Button("Back", variant="default", id="back")
                yield Button("Cancel", variant="default", id="cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            task_id_input = self.query_one("#task_id_input", Input)
            
            try:
                task_id = int(task_id_input.value)
                planner.complete_task(task_id)
                self.app.update_content(f"✅ Task {task_id} marked as done!")
                self.dismiss()
            except ValueError:
                self.app.update_content("❌ Task ID must be a number")
        elif event.button.id == "back":
            self.app.action_go_back()
            self.dismiss()
        else:
            self.dismiss()