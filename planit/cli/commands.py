"""
Typer CLI commands for PlanIt
"""

import typer
from datetime import datetime, timedelta
from typing import Optional

from rich.console import Console
from planit.core.database import TaskManager
from planit.cli.interactive import start_interactive

console = Console()
app = typer.Typer(help="PlanIt - Simple Task Manager")

# Instance globale du gestionnaire
planner = TaskManager()

@app.command()
def tui():
    """Start the Textual TUI interface"""
    console.print("[green]🚀 Starting Textual TUI...[/green]")
    from planit.tui.app import PlanItTUI
    tui_app = PlanItTUI()
    tui_app.run()

@app.command()
def add(
    title: str = typer.Argument(..., help="Task title"),
    duration: int = typer.Option(..., "--duration", "-d", help="Duration in hours"),
    recurring: bool = typer.Option(False, "--recurring", "-r", help="Is this a recurring task?"),
    days: str = typer.Option("daily", "--days", help="Which days? (mon,tue,wed,thu,fri,sat,sun or daily)"),
    start_hour: Optional[int] = typer.Option(None, "--start", "-s", help="Start hour (0-23)"),
    manual: bool = typer.Option(False, "--manual", "-m", help="Schedule manually?"),
    date: Optional[str] = typer.Option(None, "--date", help="Date for manual scheduling (MM/DD)")
):
    """Add a new task"""
    if recurring:
        if start_hour is None:
            start_hour = typer.prompt("Start hour (0-23)", type=int)
        
        if start_hour < 0 or start_hour > 23:
            console.print("[red]Error: Start hour must be between 0 and 23[/red]")
            raise typer.Exit(1)
        
        end_hour = start_hour + duration
        if end_hour > 24:
            console.print(f"[red]Error: Task would end at {end_hour}h (after midnight)[/red]")
            raise typer.Exit(1)
        
        valid_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'daily']
        if days not in valid_days and not all(day.strip() in valid_days for day in days.split(',')):
            console.print("[red]Error: Invalid days. Use mon,tue,wed,thu,fri,sat,sun or daily[/red]")
            raise typer.Exit(1)
        
        recurring_hours = f"{start_hour}-{end_hour}"
        planner.add_task(title, duration, recurring=True, recurring_days=days, recurring_hours=recurring_hours)
    
    elif manual:
        if date is None:
            date = typer.prompt("Date (MM/DD)")
        if start_hour is None:
            start_hour = typer.prompt("Start hour (0-23)", type=int)
        
        try:
            month, day = date.split('/')
            month = int(month)
            day = int(day)
            if month < 1 or month > 12 or day < 1 or day > 31:
                raise ValueError
            
            current_year = datetime.now().year
            date_obj = datetime(current_year, month, day)
            day_name = date_obj.strftime("%A")
            date_str = date_obj.strftime("%d/%m")
            
        except (ValueError, IndexError):
            console.print("[red]Error: Invalid date format. Use MM/DD[/red]")
            raise typer.Exit(1)
        
        if start_hour < 0 or start_hour > 23:
            console.print("[red]Error: Start hour must be between 0 and 23[/red]")
            raise typer.Exit(1)
        
        end_hour = start_hour + duration
        if end_hour > 24:
            console.print(f"[red]Error: Task would end at {end_hour}h (after midnight)[/red]")
            raise typer.Exit(1)
        
        manual_schedule = f"{start_hour}h-{end_hour}h"
        planner.add_task(title, duration, manual_schedule=manual_schedule, manual_date=f"{day_name} {date_str}")
    
    else:
        planner.add_task(title, duration)

@app.command()
def list():
    """Show all tasks"""
    planner.list_tasks()

@app.command()
def delete(task_id: int = typer.Argument(..., help="Task ID to delete")):
    """Delete a task"""
    planner.delete_task(task_id)

@app.command()
def done(task_id: int = typer.Argument(..., help="Task ID to mark as completed")):
    """Mark task as completed"""
    planner.complete_task(task_id)

@app.command()
def schedule():
    """Auto-schedule unscheduled tasks"""
    planner.auto_schedule()

@app.command()
def planning(
    next_week: bool = typer.Option(False, "--next", "-n", help="Show next week"),
    prev_week: bool = typer.Option(False, "--prev", "-p", help="Show previous week"),
    current: bool = typer.Option(False, "--current", "-c", help="Show current week")
):
    """Show weekly schedule"""
    if next_week:
        planner.current_week_offset += 1
    elif prev_week:
        planner.current_week_offset -= 1
    elif current:
        planner.current_week_offset = 0
    
    planner.show_schedule()

@app.command()
def next():
    """Show next week"""
    planner.current_week_offset += 1
    planner.show_schedule()

@app.command()
def prev():
    """Show previous week"""
    planner.current_week_offset -= 1
    planner.show_schedule()

@app.command()
def reset():
    """Reset schedule"""
    planner.reset_schedule()

@app.command()
def project(
    name: str = typer.Argument(..., help="Project name"),
    start_date: str = typer.Option(..., "--start", "-s", help="Start date (MM/DD)"),
    end_date: str = typer.Option(..., "--end", "-e", help="End date (MM/DD)"),
    description: str = typer.Option("", "--desc", "-d", help="Project description")
):
    """Add a new project"""
    # Validate dates
    for date_str, label in [(start_date, "start"), (end_date, "end")]:
        try:
            month, day = date_str.split('/')
            month = int(month)
            day = int(day)
            if month < 1 or month > 12 or day < 1 or day > 31:
                raise ValueError
        except (ValueError, IndexError):
            console.print(f"[red]Error: Invalid {label} date format. Use MM/DD[/red]")
            raise typer.Exit(1)
    
    planner.add_project(name, start_date, end_date, description)

@app.command()
def delproject(project_id: int = typer.Argument(..., help="Project ID to delete")):
    """Delete a project"""
    planner.delete_project(project_id)

@app.command()
def timeline():
    """Show project timeline (4 months view)"""
    planner.show_timeline()

@app.command()
def interactive():
    """Start interactive mode (original interface)"""
    console.print("[yellow]Starting interactive mode...[/yellow]")
    start_interactive()

@app.callback()
def main_callback():
    """
    PlanIt - Simple Task Manager
    
    Available interfaces:
    • CLI commands (default)
    • tui for graphical interface  
    • interactive for terminal interface
    """
    pass