"""
Planning and scheduling engine for PlanIt
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Set, Tuple

from rich.console import Console

console = Console()

class PlanningEngine:
    """
    Moteur de planification automatique
    Gère la logique de scheduling et d'affichage des plannings
    """
    
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.current_week_offset = 0
    
    def get_week_dates(self, offset=0):
        """Retourne les dates de la semaine (lundi à dimanche)"""
        today = datetime.now().date()
        # Trouve le lundi de cette semaine
        monday = today - timedelta(days=today.weekday())
        # Ajoute l'offset en semaines
        target_monday = monday + timedelta(weeks=offset)
        
        week_dates = []
        for i in range(7):
            week_dates.append(target_monday + timedelta(days=i))
        
        return week_dates
    
    def auto_schedule(self):
        """Planning automatique - seulement pour les tâches non-récurrentes"""
        conn = sqlite3.connect(self.task_manager.db_path)
        cursor = conn.cursor()
        
        # Récupère seulement les tâches NON récurrentes, non terminées et non planifiées
        cursor.execute('''
            SELECT id, title, duration
            FROM tasks
            WHERE completed = FALSE AND scheduled_time IS NULL AND recurring = FALSE
            ORDER BY id ASC
        ''')
        tasks = cursor.fetchall()
        
        # Récupère les disponibilités
        cursor.execute('SELECT day_of_week, start_hour, end_hour FROM availability ORDER BY day_of_week')
        availability = cursor.fetchall()
        
        if not tasks:
            console.print("[yellow]No non-recurring tasks to schedule.[/yellow]")
            conn.close()
            return
        
        if not availability:
            console.print("[red]No availability defined.[/red]")
            conn.close()
            return
        
        # Récupère les créneaux déjà occupés par les tâches récurrentes
        cursor.execute('''
            SELECT recurring_days, recurring_hours FROM tasks 
            WHERE recurring = TRUE AND recurring_hours IS NOT NULL
        ''')
        recurring_tasks = cursor.fetchall()
        
        # Construire une liste des créneaux occupés
        occupied_slots = set()
        days_map = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
        
        for recurring_days, recurring_hours in recurring_tasks:
            if recurring_hours and '-' in recurring_hours:
                try:
                    start_hour, end_hour = map(int, recurring_hours.split('-'))
                    if recurring_days == 'daily':
                        for day in range(7):
                            for hour in range(start_hour, end_hour):
                                occupied_slots.add((day, hour))
                    else:
                        for day_name in recurring_days.split(','):
                            day_name = day_name.strip()
                            if day_name in days_map:
                                day = days_map[day_name]
                                for hour in range(start_hour, end_hour):
                                    occupied_slots.add((day, hour))
                except ValueError:
                    continue
        
        # Planning des tâches
        scheduled_count = 0
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for task_id, title, duration in tasks:
            scheduled = False
            
            for day, start_hour, end_hour in availability:
                # Cherche un créneau libre de la durée nécessaire
                for current_hour in range(start_hour, end_hour - duration + 1):
                    # Vérifie si toutes les heures nécessaires sont libres
                    conflict = False
                    for h in range(current_hour, current_hour + duration):
                        if (day, h) in occupied_slots:
                            conflict = True
                            break
                    
                    if not conflict:
                        # Planifie la tâche
                        schedule_time = f"{days[day]} {current_hour}h-{current_hour + duration}h"
                        
                        cursor.execute('''
                            UPDATE tasks SET scheduled_time = ? WHERE id = ?
                        ''', (schedule_time, task_id))
                        
                        # Marque ces créneaux comme occupés
                        for h in range(current_hour, current_hour + duration):
                            occupied_slots.add((day, h))
                        
                        console.print(f"[green]✓[/green] {title} scheduled: [blue]{schedule_time}[/blue]")
                        scheduled_count += 1
                        scheduled = True
                        break
                
                if scheduled:
                    break
            
            if not scheduled:
                console.print(f"[red]✗[/red] Cannot schedule: {title} (duration: {duration}h)")
        
        conn.commit()
        conn.close()
        
        console.print(f"\n[bold green]{scheduled_count}[/bold green] task(s) scheduled automatically.")
    
    def show_schedule(self):
        """Affiche le planning de la semaine sous forme de tableau"""
        conn = sqlite3.connect(self.task_manager.db_path)
        cursor = conn.cursor()
        
        # Récupère toutes les tâches planifiées (récurrentes + programmées)
        cursor.execute('''
            SELECT title, scheduled_time, duration, recurring, recurring_days, recurring_hours
            FROM tasks
            WHERE (scheduled_time IS NOT NULL OR (recurring = TRUE AND recurring_hours IS NOT NULL)) 
            AND completed = FALSE
        ''')
        
        tasks = cursor.fetchall()
        conn.close()
        
        # Obtenir les dates de la semaine
        week_dates = self.get_week_dates(self.current_week_offset)
        
        # Affichage de l'en-tête avec les dates
        week_start = week_dates[0].strftime("%d/%m")
        week_end = week_dates[6].strftime("%d/%m")
        print(f"\n=== WEEKLY SCHEDULE ({week_start} - {week_end}) ===")
        
        if self.current_week_offset == 0:
            print("(Current week)")
        elif self.current_week_offset > 0:
            print(f"(+{self.current_week_offset} week{'s' if self.current_week_offset > 1 else ''})")
        else:
            print(f"({self.current_week_offset} week{'s' if self.current_week_offset < -1 else ''})")
        
        # Créer un planning par jour
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days_short = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        schedule = {day: {} for day in days}
        
        for title, scheduled_time, duration, recurring, recurring_days, recurring_hours in tasks:
            if recurring and recurring_hours:
                # Tâche récurrente
                if '-' in recurring_hours:
                    try:
                        start_hour, end_hour = map(int, recurring_hours.split('-'))
                        if recurring_days == 'daily':
                            target_days = days
                        else:
                            target_days = []
                            for day_short in recurring_days.split(','):
                                day_short = day_short.strip()
                                if day_short in days_short:
                                    target_days.append(days[days_short.index(day_short)])
                        
                        for day in target_days:
                            if day in schedule:
                                for hour in range(start_hour, end_hour):
                                    schedule[day][hour] = f"{title}"
                    except ValueError:
                        continue
            elif scheduled_time:
                # Tâche programmée
                if 'h-' in scheduled_time:
                    parts = scheduled_time.split(' ')
                    if len(parts) >= 2:
                        day_name = parts[0]
                        time_part = parts[1]
                        if 'h-' in time_part:
                            try:
                                start_str, end_str = time_part.split('-')
                                start_hour = int(start_str.replace('h', ''))
                                end_hour = int(end_str.replace('h', ''))
                                
                                if day_name in schedule:
                                    for hour in range(start_hour, end_hour):
                                        schedule[day_name][hour] = f"{title}"
                            except ValueError:
                                continue
        
        # Affichage du planning avec dates
        if not any(schedule.values()):
            print("No scheduled tasks.")
            return
        
        print("\nTime ", end="")
        for i, day in enumerate(days):
            date_str = week_dates[i].strftime("%d/%m")
            print(f"| {day[:3]} {date_str:6}", end="")
        print()
        print("-" * (6 + 13 * len(days)))
        
        for hour in range(24):
            print(f"{hour:2}h  ", end="")
            for day in days:
                task = schedule[day].get(hour, "")
                print(f"| {task[:10]:10}", end="")
            print()
        
        print(f"\nCommands: 'next' (next week) | 'prev' (previous week) | 'planning' (current week)")
    
    def get_compact_schedule_content(self) -> str:
        """
        Retourne le planning sous forme de texte compact pour l'interface TUI
        """
        conn = sqlite3.connect(self.task_manager.db_path)
        cursor = conn.cursor()
        
        # Get week dates
        week_dates = self.get_week_dates(self.current_week_offset)
        week_start = week_dates[0].strftime("%d/%m")
        week_end = week_dates[6].strftime("%d/%m")
        
        content = f"📅 SCHEDULE ({week_start} - {week_end})\n"
        
        if self.current_week_offset == 0:
            content += "(Current week)\n\n"
        elif self.current_week_offset > 0:
            content += f"(+{self.current_week_offset} week)\n\n"
        else:
            content += f"({self.current_week_offset} week)\n\n"
        
        # Get tasks
        cursor.execute('''
            SELECT title, scheduled_time, duration, recurring, recurring_days, recurring_hours
            FROM tasks
            WHERE (scheduled_time IS NOT NULL OR (recurring = TRUE AND recurring_hours IS NOT NULL)) 
            AND completed = FALSE
        ''')
        tasks = cursor.fetchall()
        conn.close()
        
        # Create schedule grid
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days_short = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        schedule = {day: {} for day in days}
        
        for title, scheduled_time, duration, recurring, recurring_days, recurring_hours in tasks:
            if recurring and recurring_hours:
                # Tâche récurrente
                if '-' in recurring_hours:
                    try:
                        start_hour, end_hour = map(int, recurring_hours.split('-'))
                        if recurring_days == 'daily':
                            target_days = days
                        else:
                            target_days = []
                            for day_short in recurring_days.split(','):
                                day_short = day_short.strip()
                                if day_short in days_short:
                                    target_days.append(days[days_short.index(day_short)])
                        
                        for day in target_days:
                            if day in schedule:
                                for hour in range(start_hour, end_hour):
                                    schedule[day][hour] = title[:6]
                    except ValueError:
                        continue
            elif scheduled_time:
                # Tâche programmée
                if 'h-' in scheduled_time:
                    parts = scheduled_time.split(' ')
                    if len(parts) >= 2:
                        day_name = parts[0]
                        time_part = parts[1]
                        if 'h-' in time_part:
                            try:
                                start_str, end_str = time_part.split('-')
                                start_hour = int(start_str.replace('h', ''))
                                end_hour = int(end_str.replace('h', ''))
                                
                                if day_name in schedule:
                                    for hour in range(start_hour, end_hour):
                                        schedule[day_name][hour] = title[:6]
                            except ValueError:
                                continue
        
        if any(schedule.values()):
            content += "Time |Mon |Tue |Wed |Thu |Fri |Sat |Sun\n"
            content += "-----|----|----|----|----|----|----|----\n"
            
            for hour in range(8, 21):
                content += f"{hour:2}h  |"
                for day in days:
                    task = schedule[day].get(hour, "")
                    content += f"{task:4}|"
                content += "\n"
                
            content += "\n📋 TASK SUMMARY:\n"
            task_summary = {}
            for day_schedule in schedule.values():
                for task in day_schedule.values():
                    if task:
                        task_summary[task] = task_summary.get(task, 0) + 1
            
            for task, hours in task_summary.items():
                content += f"• {task}: {hours}h/week\n"
        else:
            content += "No scheduled tasks for this week.\n"
        
        content += f"\nNav: Next Week (n) | Prev Week (b)"
        return content
    
    def next_week(self):
        """Passe à la semaine suivante"""
        self.current_week_offset += 1
    
    def prev_week(self):
        """Passe à la semaine précédente"""
        self.current_week_offset -= 1
    
    def current_week(self):
        """Retourne à la semaine actuelle"""
        self.current_week_offset = 0