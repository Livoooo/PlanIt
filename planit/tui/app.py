"""
Main Textual TUI application for PlanIt
"""

import sqlite3
from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Footer, Header, Static, DataTable
from textual.binding import Binding

from planit.tui.styles import TUI_CSS
from planit.tui.modals import AddTaskModal, DeleteTaskModal, AddProjectModal, MarkDoneModal
from planit.core.database import TaskManager
from planit.core.planner import PlanningEngine


class PlanItTUI(App):
    """Main Textual TUI Application"""
    
    CSS = TUI_CSS
    
    BINDINGS = [
        Binding("a", "add_task", "Add Task"),
        Binding("l", "list_tasks", "List Tasks"),
        Binding("s", "schedule", "Schedule"),
        Binding("p", "planning", "Planning"),
        Binding("t", "timeline", "Timeline"),
        Binding("j", "add_project", "Add Project"),
        Binding("n", "next_week", "Next Week"),
        Binding("b", "prev_week", "Prev Week"),
        Binding("escape", "go_back", "Back"),
        Binding("q", "quit", "Quit"),
    ]
    
    def __init__(self):
        super().__init__()
        self.task_manager = TaskManager()
        self.planner = PlanningEngine(self.task_manager)
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True)
        
        with Container(classes="container"):
            # Sidebar avec les boutons
            with Vertical(classes="sidebar"):
                yield Static("📋 PlanIt Manager", classes="title")
                yield Button("➕ Add Task", id="add_task", variant="primary")
                yield Button("📝 List Tasks", id="list_tasks", variant="default")
                yield Button("🔄 Schedule", id="schedule", variant="success")
                yield Button("📅 Planning", id="planning", variant="default")
                yield Button("⏭️ Next Week", id="next_week", variant="default")
                yield Button("⏮️ Prev Week", id="prev_week", variant="default")
                yield Button("📊 Add Project", id="add_project", variant="primary")
                yield Button("📈 Timeline", id="timeline", variant="default")
                yield Button("🗑️ Delete Task", id="delete_task", variant="error")
                yield Button("✅ Mark Done", id="mark_done", variant="warning")
                yield Button("🔄 Reset", id="reset", variant="default")
            
            # Contenu principal
            with Vertical(classes="main-content"):
                yield Static("Welcome to PlanIt! Use the sidebar buttons or keyboard shortcuts.", id="content")
                yield DataTable(id="task_table", classes="task-table")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        
        if button_id == "add_task":
            self.action_add_task()
        elif button_id == "list_tasks":
            self.action_list_tasks()
        elif button_id == "schedule":
            self.action_schedule()
        elif button_id == "planning":
            self.action_planning()
        elif button_id == "next_week":
            self.action_next_week()
        elif button_id == "prev_week":
            self.action_prev_week()
        elif button_id == "add_project":
            self.action_add_project()
        elif button_id == "timeline":
            self.action_timeline()
        elif button_id == "delete_task":
            self.action_delete_task()
        elif button_id == "mark_done":
            self.action_mark_done()
        elif button_id == "reset":
            self.action_reset()
    
    def action_add_task(self) -> None:
        """Add a new task"""
        self.push_screen(AddTaskModal())
    
    def action_list_tasks(self) -> None:
        """List all tasks in the table"""
        table = self.query_one("#task_table", DataTable)
        table.clear(columns=True)
        
        # Setup columns
        table.add_column("ID", width=5)
        table.add_column("Title", width=20)
        table.add_column("Duration", width=10)
        table.add_column("Done", width=8)
        table.add_column("Recurring", width=12)
        
        # Get tasks from database
        conn = sqlite3.connect(self.task_manager.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, duration, completed, recurring, recurring_hours
            FROM tasks
            ORDER BY recurring DESC, id ASC
        ''')
        tasks = cursor.fetchall()
        conn.close()
        
        # Add rows
        for task in tasks:
            status = "✅" if task[3] else "⭕"
            recurring = "🔄" if task[4] else "➖"
            table.add_row(
                str(task[0]),
                task[1][:18],
                f"{task[2]}h",
                status,
                recurring
            )
        
        self.update_content("📝 Task list refreshed!")
    
    def action_schedule(self) -> None:
        """Auto-schedule tasks"""
        self.planner.auto_schedule()
        self.update_content("🔄 Auto-scheduling completed!")
    
    def action_planning(self) -> None:
        """Show detailed weekly planning - optimized for TUI"""
        content = self.planner.get_compact_schedule_content()
        self.update_content(content)
    
    def action_next_week(self) -> None:
        """Show next week"""
        self.planner.next_week()
        self.action_planning()
    
    def action_prev_week(self) -> None:
        """Show previous week"""
        self.planner.prev_week()
        self.action_planning()
    
    def action_add_project(self) -> None:
        """Add a new project"""
        self.push_screen(AddProjectModal())
    
    def action_timeline(self) -> None:
        """Show compact project timeline"""
        content = "📈 PROJECT TIMELINE\n\n"
        
        conn = sqlite3.connect(self.task_manager.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, start_date, end_date, description
            FROM projects
            ORDER BY start_date ASC
        ''')
        projects = cursor.fetchall()
        conn.close()
        
        if projects:
            # Generate compact month headers (2 months only for TUI)
            current_date = datetime.now().date()
            months = []
            for i in range(2):  # Only 2 months for TUI
                month_date = current_date.replace(day=1)
                if i > 0:
                    # Add months properly
                    if month_date.month + i > 12:
                        month_date = month_date.replace(year=month_date.year + 1, month=(month_date.month + i) % 12)
                    else:
                        month_date = month_date.replace(month=month_date.month + i)
                months.append(month_date)
            
            # Compact header
            content += "ID|Project Name   |"
            for month in months:
                month_name = month.strftime("%b")
                content += f"{month_name:4}|"
            content += "\n"
            content += "--|---------------|"
            for _ in months:
                content += "----|"
            content += "\n"
            
            # Projects with compact bars
            current_year = datetime.now().year
            for project_id, name, start_str, end_str, desc in projects[:8]:  # Limit to 8 projects
                try:
                    start_month, start_day = map(int, start_str.split('/'))
                    end_month, end_day = map(int, end_str.split('/'))
                    
                    start_date = datetime(current_year, start_month, start_day).date()
                    end_date = datetime(current_year, end_month, end_day).date()
                    
                    if end_date < start_date:
                        end_date = datetime(current_year + 1, end_month, end_day).date()
                    
                    line = f"{project_id:2}|{name[:15]:15}|"
                    
                    for month in months:
                        month_start = month
                        if month.month == 12:
                            month_end = month.replace(year=month.year + 1, month=1, day=1)
                            month_end = month_end.replace(day=month_end.day - 1)
                        else:
                            month_end = month.replace(month=month.month + 1, day=1)
                            month_end = month_end.replace(day=month_end.day - 1)
                        
                        if start_date <= month_end and end_date >= month_start:
                            line += "████|"
                        else:
                            line += "    |"
                    
                    content += line + "\n"
                        
                except ValueError:
                    continue
            
            # Summary
            content += f"\n📊 {len(projects)} total projects"
            if len(projects) > 8:
                content += f" (showing first 8)"
        else:
            content += "No projects found.\n"
            content += "Press 'j' to add your first project!"
        
        content += "\n\nControls: j=Add Project"
        self.update_content(content)
    
    def action_delete_task(self) -> None:
        """Delete a task"""
        self.push_screen(DeleteTaskModal())
    
    def action_mark_done(self) -> None:
        """Mark task as done"""
        self.push_screen(MarkDoneModal())
    
    def action_reset(self) -> None:
        """Reset schedule"""
        self.task_manager.reset_schedule()
        self.update_content("🔄 Schedule reset completed!")
    
    def action_go_back(self) -> None:
        """Go back to main interface"""
        self.update_content("📋 Welcome back to PlanIt! Use the sidebar buttons or keyboard shortcuts.")
    
    def update_content(self, message: str) -> None:
        """Update the main content area"""
        content_widget = self.query_one("#content", Static)
        content_widget.update(message)