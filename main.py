#!/usr/bin/env python3
"""
PlanIt - Point d'entrée principal
Simple Task Manager and Scheduler

Usage:
    python main.py --help           # Show all commands
    python main.py tui              # Launch TUI interface
    python main.py interactive      # Launch interactive mode
    python main.py add "Study" -d 2 # Add a task via CLI
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from planit.cli.commands import app
    from planit.utils.console import console, print_welcome, print_error
except ImportError as e:
    print(f"Error importing PlanIt modules: {e}")
    print("Make sure you're running from the project root directory.")
    sys.exit(1)

def main():
    """Point d'entrée principal de PlanIt"""
    try:
        # If no arguments provided, show welcome and help
        if len(sys.argv) == 1:
            print_welcome()
            console.print("\n[dim]Use --help to see available commands or 'tui' for graphical interface[/dim]")
            console.print("[dim]Examples:[/dim]")
            console.print("  [cyan]python main.py tui[/cyan]                    # Launch TUI")
            console.print("  [cyan]python main.py interactive[/cyan]            # Interactive mode")
            console.print("  [cyan]python main.py add 'Study' -d 2[/cyan]      # Add task")
            console.print("  [cyan]python main.py --help[/cyan]                # Full help")
            return
        
        # Launch Typer CLI
        app()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {e}")
        console.print("[dim]Use --help for usage information[/dim]")
        sys.exit(1)

if __name__ == "__main__":
    main()