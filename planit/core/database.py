"""
Database management and task operations for PlanIt
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

from rich.console import Console
from rich.table import Table

console = Console()

class TaskManager:
    """
    Gestionnaire de base de données pour les tâches et projets
    Anciennement classe PlanIt
    """
    
    def __init__(self, db_path="planit.db"):
        self.db_path = db_path
        self.current_week_offset = 0  # 0 = semaine actuelle, 1 = suivante, -1 = précédente
        self.init_database()
        self.init_default_availability()
    
    def init_database(self):
        """Initialise la base de données SQLite"""
        console.print(f"[blue]Initializing database at:[/blue] {self.db_path}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Debug: vérifie si les tables existent déjà
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = cursor.fetchall()
        console.print(f"[dim]Existing tables:[/dim] {existing_tables}")
        
        # Ne plus supprimer les tables - juste les créer si elles n'existent pas
        # Table des tâches
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                duration INTEGER NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                scheduled_time TEXT,
                recurring BOOLEAN DEFAULT FALSE,
                recurring_days TEXT,
                recurring_hours TEXT
            )
        ''')
        
        # Table des projets
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                description TEXT
            )
        ''')
        
        # Table des disponibilités
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS availability (
                day_of_week INTEGER,
                start_hour INTEGER,
                end_hour INTEGER
            )
        ''')
        
        # Debug: vérifie le contenu des tables après création
        cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM availability")
        avail_count = cursor.fetchone()[0]
        console.print(f"[dim]Tasks count:[/dim] {task_count}, [dim]Availability count:[/dim] {avail_count}")
        
        conn.commit()
        conn.close()
    
    def init_default_availability(self):
        """Initialise une disponibilité par défaut (9h-18h du lundi au vendredi) SEULEMENT si aucune n'existe"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Vérifie si des disponibilités existent déjà
        cursor.execute('SELECT COUNT(*) FROM availability')
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Ajoute une dispo par défaut : 9h-18h du lundi au vendredi
            default_schedule = [
                (0, 9, 18),   # Lundi
                (1, 9, 18),   # Mardi
                (2, 9, 18),   # Mercredi
                (3, 9, 18),   # Jeudi
                (4, 9, 18),   # Vendredi
            ]
            
            for day, start, end in default_schedule:
                cursor.execute('''
                    INSERT INTO availability (day_of_week, start_hour, end_hour)
                    VALUES (?, ?, ?)
                ''', (day, start, end))
            
            console.print("[green]✓[/green] Default availability created: 9h-18h Monday to Friday")
        # Si des disponibilités existent déjà, ne rien faire (pas de message)
        
        conn.commit()
        conn.close()
    
    def add_task(self, title: str, duration: int, recurring: bool = False, recurring_days: str = None, recurring_hours: str = None, manual_schedule: str = None, manual_date: str = None):
        """Ajoute une nouvelle tâche"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Si c'est une tâche manuelle avec date, formater le scheduled_time
        if manual_schedule and manual_date:
            manual_schedule = f"{manual_date} {manual_schedule}"
        
        try:
            cursor.execute('''
                INSERT INTO tasks (title, duration, recurring, recurring_days, recurring_hours, scheduled_time)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, duration, recurring, recurring_days, recurring_hours, manual_schedule))
            
            conn.commit()
            
            if recurring:
                console.print(f"[green]✓[/green] Recurring task added: [bold]{title}[/bold] ({recurring_days} at {recurring_hours})")
            elif manual_schedule:
                console.print(f"[green]✓[/green] Task manually scheduled: [bold]{title}[/bold] at {manual_schedule}")
            else:
                console.print(f"[green]✓[/green] Task added: [bold]{title}[/bold]")
                
        except Exception as e:
            print(f"Error adding task: {e}")
        finally:
            conn.close()
    
    def list_tasks(self):
        """Affiche toutes les tâches avec Rich"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, title, duration, completed, scheduled_time, recurring, recurring_hours
                FROM tasks
                ORDER BY recurring DESC, id ASC
            ''')
            
            tasks = cursor.fetchall()
            
            if not tasks:
                console.print("[yellow]No tasks found.[/yellow]")
                return
            
            # Créer un tableau Rich
            table = Table(title="📋 Task List")
            table.add_column("ID", style="cyan", width=3)
            table.add_column("Title", style="magenta", width=15)
            table.add_column("Duration(h)", style="green", width=12)
            table.add_column("Done", style="yellow", width=6)
            table.add_column("Scheduled", style="blue", width=15)
            table.add_column("Recurring", style="red", width=12)
            
            for task in tasks:
                status = "[green]✓[/green]" if task[3] else "[red]○[/red]"
                scheduled = task[4] if task[4] else "[dim]Not scheduled[/dim]"
                if task[5]:  # recurring
                    recurring_info = f"[green]Yes[/green] ({task[6]})" if task[6] else "[green]Yes[/green]"
                else:
                    recurring_info = "[dim]No[/dim]"
                
                table.add_row(
                    str(task[0]),
                    task[1][:15],
                    str(task[2]),
                    status,
                    scheduled[:15],
                    recurring_info
                )
            
            console.print(table)
                
        except Exception as e:
            console.print(f"[red]Error listing tasks: {e}[/red]")
        finally:
            conn.close()
    
    def delete_task(self, task_id: int):
        """Supprime une tâche"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            
            if cursor.rowcount > 0:
                console.print(f"[green]✓[/green] Task {task_id} deleted")
            else:
                console.print(f"[red]✗[/red] Task {task_id} not found")
            
            conn.commit()
        except Exception as e:
            print(f"Error deleting task: {e}")
        finally:
            conn.close()
    
    def complete_task(self, task_id: int):
        """Marque une tâche comme terminée"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('UPDATE tasks SET completed = TRUE WHERE id = ?', (task_id,))
            
            if cursor.rowcount > 0:
                console.print(f"[green]✓[/green] Task {task_id} marked as done")
            else:
                console.print(f"[red]✗[/red] Task {task_id} not found")
            
            conn.commit()
        except Exception as e:
            print(f"Error completing task: {e}")
        finally:
            conn.close()
    
    def add_project(self, name: str, start_date: str, end_date: str, description: str = ""):
        """Ajoute un nouveau projet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO projects (name, start_date, end_date, description)
                VALUES (?, ?, ?, ?)
            ''', (name, start_date, end_date, description))
            
            conn.commit()
            print(f"✓ Project added: {name} ({start_date} → {end_date})")
                
        except Exception as e:
            print(f"Error adding project: {e}")
        finally:
            conn.close()
    
    def delete_project(self, project_id: int):
        """Supprime un projet"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
            
            if cursor.rowcount > 0:
                print(f"✓ Project {project_id} deleted")
            else:
                print(f"✗ Project {project_id} not found")
            
            conn.commit()
        except Exception as e:
            print(f"Error deleting project: {e}")
        finally:
            conn.close()
    
    def show_timeline(self):
        """Affiche la timeline des projets sur 4 mois avec les IDs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, name, start_date, end_date, description
                FROM projects
                ORDER BY start_date ASC
            ''')
            
            projects = cursor.fetchall()
            
            if not projects:
                print("No projects to display in timeline.")
                return
            
            print("\n=== PROJECT TIMELINE (Next 4 Months) ===")
            
            # Générer les 4 prochains mois
            current_date = datetime.now().date()
            months = []
            for i in range(4):
                month_date = current_date.replace(day=1) + timedelta(days=32*i)
                month_date = month_date.replace(day=1)  # Premier du mois
                months.append(month_date)
            
            # En-tête avec les mois
            header = "ID │ Project Name        │"
            month_names = []
            for month in months:
                month_name = month.strftime("%b %Y")
                month_names.append(month_name)
                header += f" {month_name:8} │"
            
            print(header)
            print("─" * len(header))
            
            current_year = datetime.now().year
            
            # Traiter chaque projet
            for project_id, name, start_str, end_str, desc in projects:
                try:
                    start_month, start_day = map(int, start_str.split('/'))
                    end_month, end_day = map(int, end_str.split('/'))
                    
                    start_date = datetime(current_year, start_month, start_day).date()
                    end_date = datetime(current_year, end_month, end_day).date()
                    
                    # Si la date de fin est avant le début, considérer l'année suivante
                    if end_date < start_date:
                        end_date = datetime(current_year + 1, end_month, end_day).date()
                    
                    # Ligne du projet avec ID
                    line = f"{project_id:2} │ {name[:18]:18} │"
                    
                    for month in months:
                        month_start = month
                        # Dernier jour du mois
                        if month.month == 12:
                            month_end = month.replace(year=month.year + 1, month=1, day=1) - timedelta(days=1)
                        else:
                            month_end = month.replace(month=month.month + 1, day=1) - timedelta(days=1)
                        
                        # Vérifier si le projet chevauche ce mois
                        if start_date <= month_end and end_date >= month_start:
                            # Calculer la position dans le mois
                            overlap_start = max(start_date, month_start)
                            overlap_end = min(end_date, month_end)
                            
                            # Position relative dans le mois (0-8 caractères)
                            days_in_month = (month_end - month_start).days + 1
                            start_pos = ((overlap_start - month_start).days / days_in_month) * 8
                            end_pos = ((overlap_end - month_start).days / days_in_month) * 8
                            
                            # Créer la barre visuelle
                            bar = [' '] * 8
                            for i in range(int(start_pos), min(8, int(end_pos) + 1)):
                                if i == int(start_pos):
                                    bar[i] = '├'  # Début
                                elif i == int(end_pos) or i == 7:
                                    bar[i] = '┤'  # Fin
                                else:
                                    bar[i] = '─'  # Milieu
                            
                            line += f" {''.join(bar)} │"
                        else:
                            line += f" {' ':8} │"
                    
                    print(line)
                    if desc:
                        desc_line = f"   │ {desc[:18]:18} │"
                        for _ in months:
                            desc_line += f" {' ':8} │"
                        print(desc_line)
                    
                except ValueError:
                    continue
            
            print(f"\nUse 'delproject <ID>' to delete a project")
                
        except Exception as e:
            print(f"Error showing timeline: {e}")
        finally:
            conn.close()
    
    def reset_schedule(self):
        """Remet à zéro la planification"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE tasks SET scheduled_time = NULL')
        conn.commit()
        conn.close()
        
        print("✓ Schedule reset")