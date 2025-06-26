"""
Interactive terminal mode for PlanIt
"""

from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from planit.core.database import TaskManager

console = Console()

def start_interactive():
    """Mode interactif original de PlanIt"""
    
    planner = TaskManager()
    
    welcome_panel = Panel.fit(
        "[bold blue]PLANIT[/bold blue] - Simple Task Manager\n"
        "Type '[yellow]help[/yellow]' to see available commands",
        border_style="blue"
    )
    console.print(welcome_panel)
    
    while True:
        try:
            user_input = input("\n> ").strip()
            command = user_input.lower().split()[0] if user_input else ""
            
            if command in ['help', 'h']:
                help_table = Table(title="🛠️ Available Commands")
                help_table.add_column("Command", style="cyan", width=15)
                help_table.add_column("Description", style="white", width=40)
                
                commands = [
                    ("add", "Add a new task (recurring, manual schedule, or auto)"),
                    ("list", "Show all tasks"),
                    ("del", "Delete a task"),
                    ("done", "Mark task as completed"),
                    ("schedule", "Auto-schedule unscheduled tasks"),
                    ("planning", "Show current week schedule"),
                    ("next", "Show next week"),
                    ("prev", "Show previous week"),
                    ("reset", "Reset schedule"),
                    ("project", "Add a new project"),
                    ("delproject", "Delete a project"),
                    ("timeline", "Show project timeline (4 months view)"),
                    ("quit", "Exit application")
                ]
                
                for cmd, desc in commands:
                    help_table.add_row(cmd, desc)
                
                console.print(help_table)
            
            elif command == 'add':
                title = input("Task title: ")
                try:
                    duration = int(input("Duration (hours): "))
                except ValueError:
                    console.print("[red]Error: Duration must be a number[/red]")
                    continue
                    
                recurring = input("Recurring task? (y/n): ").strip().lower() == 'y'
                
                if recurring:
                    recurring_days = input("Which days? (mon,tue,wed,thu,fri,sat,sun or daily): ").strip().lower()
                    valid_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun', 'daily']
                    if recurring_days not in valid_days and not all(day.strip() in valid_days for day in recurring_days.split(',')):
                        console.print("[red]Error: Invalid days. Use mon,tue,wed,thu,fri,sat,sun or daily[/red]")
                        continue
                    
                    try:
                        start_hour = int(input("Start hour (0-23): "))
                        if start_hour < 0 or start_hour > 23:
                            raise ValueError
                        
                        end_hour = start_hour + duration
                        if end_hour > 24:
                            console.print(f"[red]Error: Task would end at {end_hour}h (after midnight)[/red]")
                            continue
                            
                    except ValueError:
                        console.print("[red]Error: Start hour must be a number between 0 and 23[/red]")
                        continue
                    
                    recurring_hours = f"{start_hour}-{end_hour}"
                    planner.add_task(title, duration, recurring=True, recurring_days=recurring_days, recurring_hours=recurring_hours)
                else:
                    manual = input("Schedule manually? (y/n): ").strip().lower() == 'y'
                    
                    if manual:
                        date_input = input("Date (MM/DD): ").strip()
                        try:
                            month, day = date_input.split('/')
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
                            continue
                        
                        try:
                            start_hour = int(input("Start hour (0-23): "))
                            if start_hour < 0 or start_hour > 23:
                                raise ValueError
                            
                            end_hour = start_hour + duration
                            if end_hour > 24:
                                console.print(f"[red]Error: Task would end at {end_hour}h (after midnight)[/red]")
                                continue
                                
                        except ValueError:
                            console.print("[red]Error: Start hour must be a number between 0 and 23[/red]")
                            continue
                        
                        manual_schedule = f"{start_hour}h-{end_hour}h"
                        planner.add_task(title, duration, manual_schedule=manual_schedule, manual_date=f"{day_name} {date_str}")
                    else:
                        planner.add_task(title, duration)
            
            elif command in ['list', 'ls']:
                planner.list_tasks()
            
            elif command in ['del', 'delete', 'rm']:
                task_id = int(input("Task ID to delete: "))
                planner.delete_task(task_id)
            
            elif command in ['done', 'complete']:
                task_id = int(input("Task ID completed: "))
                planner.complete_task(task_id)
            
            elif command in ['schedule', 'auto']:
                planner.auto_schedule()
            
            elif command in ['next', 'prev', 'previous']:
                if command in ['next', 'n']:
                    planner.current_week_offset += 1
                elif command in ['prev', 'previous', 'p']:
                    planner.current_week_offset -= 1
                planner.show_schedule()
            
            elif command == 'planning':
                if len(user_input.split()) > 1:
                    arg = user_input.split()[1].lower()
                    if arg in ['next', 'n']:
                        planner.current_week_offset += 1
                    elif arg in ['prev', 'previous', 'p']:
                        planner.current_week_offset -= 1
                    elif arg == 'current':
                        planner.current_week_offset = 0
                
                planner.show_schedule()
            
            elif command == 'reset':
                planner.reset_schedule()
            
            elif command == 'project':
                name = input("Project name: ")
                
                start_date = input("Start date (MM/DD): ").strip()
                try:
                    month, day = start_date.split('/')
                    month = int(month)
                    day = int(day)
                    if month < 1 or month > 12 or day < 1 or day > 31:
                        raise ValueError
                except (ValueError, IndexError):
                    print("Error: Invalid start date format. Use MM/DD")
                    continue
                
                end_date = input("End date (MM/DD): ").strip()
                try:
                    month, day = end_date.split('/')
                    month = int(month)
                    day = int(day)
                    if month < 1 or month > 12 or day < 1 or day > 31:
                        raise ValueError
                except (ValueError, IndexError):
                    print("Error: Invalid end date format. Use MM/DD")
                    continue
                
                description = input("Description (optional): ").strip()
                planner.add_project(name, start_date, end_date, description)
            
            elif command in ['delproject', 'deleteproject']:
                if len(user_input.split()) > 1:
                    try:
                        project_id = int(user_input.split()[1])
                        planner.delete_project(project_id)
                    except (ValueError, IndexError):
                        print("Error: Usage 'delproject <ID>' or just 'delproject'")
                else:
                    try:
                        project_id = int(input("Project ID to delete: "))
                        planner.delete_project(project_id)
                    except ValueError:
                        print("Error: Project ID must be a number")
            
            elif command in ['timeline', 'view']:
                planner.show_timeline()
            
            elif command in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            else:
                print("Unknown command. Type 'help' for commands.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")