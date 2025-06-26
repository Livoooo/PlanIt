"""
Rich console configuration and utilities for PlanIt
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Configuration globale de Rich
console = Console()

def print_welcome():
    """Affiche le message de bienvenue PlanIt"""
    welcome_panel = Panel.fit(
        "[bold blue]PLANIT[/bold blue] - Simple Task Manager\n"
        "A lightweight terminal-based task manager and scheduler",
        border_style="blue",
        title="🚀 Welcome"
    )
    console.print(welcome_panel)

def print_success(message: str):
    """Affiche un message de succès"""
    console.print(f"[green]✓[/green] {message}")

def print_error(message: str):
    """Affiche un message d'erreur"""
    console.print(f"[red]✗[/red] {message}")

def print_warning(message: str):
    """Affiche un message d'avertissement"""
    console.print(f"[yellow]⚠[/yellow] {message}")

def print_info(message: str):
    """Affiche un message d'information"""
    console.print(f"[blue]ℹ[/blue] {message}")

def create_help_table():
    """Crée un tableau d'aide pour les commandes"""
    table = Table(title="🛠️ Available Commands")
    table.add_column("Command", style="cyan", width=15)
    table.add_column("Description", style="white", width=40)
    table.add_column("Example", style="dim", width=25)
    
    commands = [
        ("add", "Add a new task", "planit add 'Study' -d 2"),
        ("list", "Show all tasks", "planit list"),
        ("delete", "Delete a task", "planit delete 1"),
        ("done", "Mark task as completed", "planit done 1"),
        ("schedule", "Auto-schedule tasks", "planit schedule"),
        ("planning", "Show weekly schedule", "planit planning"),
        ("project", "Add a new project", "planit project 'Web App' -s 06/01 -e 08/31"),
        ("timeline", "Show project timeline", "planit timeline"),
        ("tui", "Launch graphical interface", "planit tui"),
        ("interactive", "Launch interactive mode", "planit interactive")
    ]
    
    for cmd, desc, example in commands:
        table.add_row(cmd, desc, example)
    
    return table

def format_duration(hours: int) -> str:
    """Formate une durée en heures de manière lisible"""
    if hours == 1:
        return "1 hour"
    elif hours < 24:
        return f"{hours} hours"
    else:
        days = hours // 24
        remaining_hours = hours % 24
        if days == 1 and remaining_hours == 0:
            return "1 day"
        elif remaining_hours == 0:
            return f"{days} days"
        else:
            return f"{days}d {remaining_hours}h"

def format_task_status(completed: bool) -> str:
    """Formate le statut d'une tâche"""
    return "[green]✓ Done[/green]" if completed else "[yellow]○ Pending[/yellow]"

def print_task_summary(total_tasks: int, completed_tasks: int, pending_tasks: int):
    """Affiche un résumé des tâches"""
    panel_content = f"""
[bold]📊 Task Summary[/bold]

Total tasks: [cyan]{total_tasks}[/cyan]
Completed: [green]{completed_tasks}[/green]
Pending: [yellow]{pending_tasks}[/yellow]
Progress: [blue]{(completed_tasks/total_tasks*100) if total_tasks > 0 else 0:.1f}%[/blue]
    """.strip()
    
    console.print(Panel(panel_content, border_style="green"))