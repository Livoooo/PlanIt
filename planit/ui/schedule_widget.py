from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Static, Button, Label, Input, Select
from textual.events import Click, MouseUp, MouseMove
from textual.reactive import reactive
from textual.message import Message
from textual.screen import ModalScreen
from datetime import datetime, time
from typing import Optional, Set, Tuple, List

class TimeSlotCell(Button):
    """Cellule représentant un créneau horaire dans la grille"""
    
    def __init__(self, day: str, hour: int, **kwargs):
        content = "░"
        super().__init__(content, **kwargs)
        self.day = day
        self.hour = hour
        self.is_selected = False
        self.is_busy = False
        self.task_name = ""
        self.task_type = "task"
        self.add_class("time-cell")
        self.can_focus = False
    
    def update_display(self):
        """Met à jour l'affichage de la cellule"""
        if self.is_busy:
            # Couleurs différentes selon le type
            if self.task_type == "course":
                self.label = f"[blue]{self.task_name[:6]}[/blue]"
                self.variant = "primary"
            elif self.task_type == "meeting":
                self.label = f"[red]{self.task_name[:6]}[/red]"
                self.variant = "error"
            elif self.task_type == "sport":
                self.label = f"[green]{self.task_name[:6]}[/green]"
                self.variant = "success"
            elif self.task_type == "break":
                self.label = f"[yellow]{self.task_name[:6]}[/yellow]"
                self.variant = "warning"
            elif self.task_type == "free":
                self.label = f"[cyan]Libre[/cyan]"
                self.variant = "default"
            else:  # task ou autres
                self.label = f"[white]{self.task_name[:6]}[/white]"
                self.variant = "default"
        elif self.is_selected:
            self.label = "[green]●[/green]"
            self.variant = "success"
        else:
            self.label = "░"
            self.variant = "default"
        
        # Forcer la mise à jour de l'affichage
        self.refresh(layout=True)
    
    def toggle_selected(self):
        """Basculer la sélection de cette cellule"""
        if not self.is_busy:
            self.is_selected = not self.is_selected
            self.update_display()
    
    def set_selected(self, selected: bool):
        """Définir l'état de sélection"""
        if not self.is_busy:
            self.is_selected = selected
            self.update_display()
    
    def set_busy(self, task_name: str, task_type: str = "task"):
        """Marquer cette cellule comme occupée avec nom et type"""
        self.is_busy = True
        self.task_name = task_name
        self.task_type = task_type
        self.is_selected = False
        self.update_display()

class TaskDialog(ModalScreen):
    """Dialogue pour ajouter une tâche aux créneaux sélectionnés"""
    
    CSS = """
    TaskDialog {
        align: center middle;
    }
    
    #dialog {
        width: 80;
        height: 28;
        border: thick $primary;
        background: $surface;
        padding: 3;
    }
    
    #dialog-title {
        text-style: bold;
        text-align: center;
        background: $boost;
        padding: 1;
        margin: 0 0 2 0;
    }
    
    .dialog-label {
        text-style: bold;
        margin: 1 0 1 0;
    }
    
    #task-input {
        width: 100%;
        margin: 0 0 2 0;
        height: 3;
    }
    
    #task-input.error {
        border: thick red;
    }
    
    #task-type {
        width: 100%;
        margin: 0 0 3 0;
        height: 3;
    }
    
    .dialog-buttons {
        width: 100%;
        height: 5;
        margin: 3 0 0 0;
    }
    
    .dialog-buttons Button {
        width: 1fr;
        margin: 0 2;
        height: 4;
    }
    """
    
    def __init__(self, selection_text: str, selection: Set[Tuple[str, int]]):
        super().__init__()
        self.selection_text = selection_text
        self.selection = selection
        self.task_name = ""
        self.task_type = "task"
    
    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Label(f"Ajouter à: {self.selection_text}", id="dialog-title")
            yield Label("Nom de la tâche/événement:", classes="dialog-label")
            yield Input(placeholder="Ex: Réviser mathématiques, Réunion équipe...", id="task-input")
            
            yield Label("Type:", classes="dialog-label")
            yield Select([
                ("Tâche", "task"),
                ("Cours", "course"), 
                ("Réunion", "meeting"),
                ("Pause", "break"),
                ("Sport", "sport"),
                ("Personnel", "personal"),
                ("Libre", "free")
            ], value="task", id="task-type")
            
            with Horizontal(classes="dialog-buttons"):
                yield Button("✅ Accepter", id="accept-btn", variant="success")
                yield Button("🔙 Retour", id="back-btn", variant="warning")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "accept-btn":
            task_input = self.query_one("#task-input", Input)
            type_select = self.query_one("#task-type", Select)
            
            if task_input.value.strip():
                self.task_name = task_input.value.strip()
                self.task_type = type_select.value
                self.dismiss({"name": self.task_name, "type": self.task_type, "selection": self.selection})
            else:
                # Highlight l'input si vide
                task_input.add_class("error")
                # Afficher un message d'erreur
                title_label = self.query_one("#dialog-title", Label)
                title_label.update("❌ Veuillez saisir un nom de tâche")
        
        elif event.button.id == "back-btn":
            self.dismiss(None)
    
    def on_input_changed(self, event: Input.Changed) -> None:
        # Enlever le style d'erreur quand l'utilisateur tape
        if event.input.id == "task-input":
            event.input.remove_class("error")
            # Remettre le titre normal
            title_label = self.query_one("#dialog-title", Label)
            title_label.update(f"Ajouter à: {self.selection_text}")
    
    def on_key(self, event) -> None:
        """Gérer les raccourcis clavier dans le dialogue"""
        if event.key == "enter":
            # Accepter directement
            task_input = self.query_one("#task-input", Input)
            type_select = self.query_one("#task-type", Select)
            
            if task_input.value.strip():
                self.task_name = task_input.value.strip()
                self.task_type = type_select.value
                self.dismiss({"name": self.task_name, "type": self.task_type, "selection": self.selection})
        elif event.key == "escape":
            # Retour directement
            self.dismiss(None)

class ScheduleGrid(Container):
    """Grille interactive pour l'emploi du temps"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        self.hours = list(range(8, 21))  # 8h à 20h
        self.cells = {}  # {(day, hour): TimeSlotCell}
        self.current_selection: Set[Tuple[str, int]] = set()
        self.selection_start: Optional[Tuple[str, int]] = None
        self.is_selecting = False
        self.remove_mode = False  # Mode pour enlever les sélections
    
    def compose(self) -> ComposeResult:
        """Construire la grille de l'emploi du temps"""
        with ScrollableContainer():
            with Vertical(id="schedule-container"):
                # En-tête avec les jours
                with Horizontal(classes="header-row"):
                    yield Label("Heure", classes="time-header")
                    for day in self.days:
                        yield Label(day[:3], classes="day-header")  # Abréger les noms
                
                # Lignes pour chaque heure
                for hour in self.hours:
                    with Horizontal(classes="time-row"):
                        yield Label(f"{hour:02d}:00", classes="time-label")
                        for day in self.days:
                            cell = TimeSlotCell(day, hour)
                            cell.id = f"cell-{day}-{hour}"
                            self.cells[(day, hour)] = cell
                            yield cell
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Gérer les clics sur les cellules"""
        # Trouver quelle cellule a été cliquée
        for (day, hour), cell in self.cells.items():
            if cell == event.button:
                self._handle_cell_click(day, hour, cell)
                break
    
    def _handle_cell_click(self, day: str, hour: int, cell: TimeSlotCell):
        """Gérer le clic sur une cellule"""
        # Si la cellule est occupée, afficher les détails
        if cell.is_busy:
            self._show_task_details(day, hour, cell)
            return
        
        # Si la cellule est déjà sélectionnée, la désélectionner
        if cell.is_selected:
            self.current_selection.discard((day, hour))
            cell.set_selected(False)
            self._update_selection_display()
            return
        
        # Si c'est un clic simple (pas en train de sélectionner)
        if not self.is_selecting:
            # Démarrer une nouvelle sélection
            self.is_selecting = True
            self.selection_start = (day, hour)
            self.current_selection.add((day, hour))
            cell.set_selected(True)
            self._update_selection_display()
        
        else:
            # On est en train de sélectionner, étendre la sélection
            if self.selection_start and self.selection_start[0] == day:
                # Même jour : sélectionner la plage
                start_hour = self.selection_start[1]
                end_hour = hour
                
                min_hour = min(start_hour, end_hour)
                max_hour = max(start_hour, end_hour)
                
                # Effacer l'ancienne sélection sur ce jour
                old_selection = {(d, h) for d, h in self.current_selection if d == day}
                for d, h in old_selection:
                    self.current_selection.remove((d, h))
                    if (d, h) in self.cells:
                        self.cells[(d, h)].set_selected(False)
                
                # Créer la nouvelle sélection
                for h in range(min_hour, max_hour + 1):
                    if (day, h) in self.cells and not self.cells[(day, h)].is_busy:
                        self.current_selection.add((day, h))
                        self.cells[(day, h)].set_selected(True)
            
            else:
                # Jour différent : ajouter juste cette cellule
                self.current_selection.add((day, hour))
                cell.set_selected(True)
            
            self._update_selection_display()
    
    def _show_task_details(self, day: str, hour: int, cell: TimeSlotCell):
        """Afficher les détails d'une tâche"""
        if hasattr(self, 'app') and self.app:
            try:
                selection_label = self.app.query_one("#selection-display", Label)
                details = f"📋 {cell.task_name} • {day} {hour:02d}h • Type: {getattr(cell, 'task_type', 'task')}"
                selection_label.update(details)
            except:
                pass
    
    def _clear_selection(self):
        """Effacer la sélection actuelle"""
        for day, hour in self.current_selection:
            if (day, hour) in self.cells:
                self.cells[(day, hour)].set_selected(False)
        self.current_selection.clear()
    
    def _update_selection_display(self):
        """Mettre à jour l'affichage sans message"""
        if self.current_selection:
            selection_text = self._format_selection()
            # Mettre à jour directement via l'app parent
            if hasattr(self, 'app') and self.app:
                try:
                    selection_label = self.app.query_one("#selection-display", Label)
                    selection_label.update(f"Sélection: {selection_text}")
                except:
                    pass
    
    def _format_selection(self) -> str:
        """Formater la sélection en texte lisible"""
        if not self.current_selection:
            return ""
        
        # Grouper par jour
        by_day = {}
        for day, hour in self.current_selection:
            if day not in by_day:
                by_day[day] = []
            by_day[day].append(hour)
        
        parts = []
        for day, hours in by_day.items():
            hours.sort()
            if len(hours) == 1:
                parts.append(f"{day[:3]} {hours[0]:02d}h")
            else:
                parts.append(f"{day[:3]} {hours[0]:02d}h-{hours[-1]+1:02d}h")
        
        return ", ".join(parts)
    
    def add_task_to_schedule(self, day: str, hour: int, task_name: str, task_type: str = "task"):
        """Ajouter une tâche à l'emploi du temps"""
        if (day, hour) in self.cells:
            cell = self.cells[(day, hour)]
            cell.set_busy(task_name, task_type)
            # Debug : vérifier que la cellule est bien mise à jour
            print(f"Cellule {day} {hour}h mise à jour: {cell.task_name} ({cell.task_type}) - busy: {cell.is_busy}")
        else:
            print(f"Erreur: cellule {day} {hour}h non trouvée")
    
    def clear_current_selection(self):
        """Effacer la sélection actuelle (appelé depuis l'extérieur)"""
        self._clear_selection()
        self.is_selecting = False
        self.selection_start = None

class InteractiveScheduleApp(App):
    """Application principale pour l'emploi du temps interactif"""
    
    CSS = """
    Screen {
        layout: vertical;
        align: center top;
    }
    
    #schedule-container {
        width: 95%;
        height: auto;
        border: thick $primary;
        margin: 2;
        padding: 1;
    }
    
    .time-cell {
        width: 10;
        height: 1;
        min-width: 10;
        margin: 0;
        padding: 0;
        text-align: center;
    }
    
    .time-header, .day-header {
        width: 10;
        height: 1;
        text-align: center;
        background: $boost;
        color: $text;
        text-style: bold;
        padding: 0;
        margin: 0;
    }
    
    .time-label {
        width: 10;
        height: 1;
        text-align: center;
        background: $surface;
        padding: 0;
        margin: 0;
        text-style: bold;
        color: $text;
    }
    
    .header-row, .time-row {
        height: 1;
        width: 100%;
        margin: 0;
        padding: 0;
        align: center top;
    }
    
    .status-bar {
        height: 5;
        width: 95%;
        background: $surface;
        padding: 1;
        border: solid $secondary;
        margin: 1;
        text-align: center;
    }
    
    .controls {
        height: 3;
        width: 95%;
        background: $panel;
        padding: 1;
        border: solid $secondary;
        margin: 1;
        text-align: center;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.selection_text = reactive("")
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container():
            yield ScheduleGrid(id="schedule-grid")
            
            with Container(classes="status-bar"):
                yield Label("🖱️ Sélectionner créneaux • Clic sur tâche = détails • ESC = effacer • Entrée = ajouter", id="instruction")
                yield Label("", id="selection-display")
            
            with Horizontal(classes="controls"):
                yield Button("Confirmer sélection", id="confirm-btn", variant="success")
                yield Button("Effacer tout", id="clear-btn", variant="warning")
                yield Button("Mode enlever", id="remove-mode-btn", variant="primary")
                yield Button("Quitter", id="quit-btn", variant="error")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Gérer les clics sur les boutons"""
        if event.button.id == "quit-btn":
            self.exit()
        elif event.button.id == "clear-btn":
            self._clear_selection()
        elif event.button.id == "confirm-btn":
            self._confirm_selection()
        elif event.button.id == "remove-mode-btn":
            self._toggle_remove_mode()
    
    def _toggle_remove_mode(self):
        """Basculer le mode enlever"""
        grid = self.query_one("#schedule-grid", ScheduleGrid)
        grid.remove_mode = not grid.remove_mode
        
        remove_btn = self.query_one("#remove-mode-btn", Button)
        instruction = self.query_one("#instruction", Label)
        
        if grid.remove_mode:
            remove_btn.label = "Mode normal"
            remove_btn.variant = "error"
            instruction.update("🗑️ MODE ENLEVER : Cliquez sur les cases à enlever de la sélection")
        else:
            remove_btn.label = "Mode enlever"
            remove_btn.variant = "primary"
            instruction.update("🖱️ Sélectionner créneaux • Clic sur tâche = détails • ESC = effacer • Entrée = ajouter")
    
    def on_key(self, event) -> None:
        """Gérer les raccourcis clavier"""
        if event.key == "escape":
            self._clear_selection()
        elif event.key == "enter":
            self._confirm_selection()
        elif event.key == "r":
            self._toggle_remove_mode()
        elif event.key == "q":
            self.exit()
    
    # Méthode supprimée car on n'utilise plus le système de messages
    
    def _clear_selection(self):
        """Effacer la sélection actuelle"""
        grid = self.query_one("#schedule-grid", ScheduleGrid)
        grid.clear_current_selection()
        
        selection_label = self.query_one("#selection-display", Label)
        selection_label.update("")
    
    def _confirm_selection(self):
        """Confirmer et sauvegarder la sélection"""
        grid = self.query_one("#schedule-grid", ScheduleGrid)
        if grid.current_selection:
            selection_text = grid._format_selection()
            
            # Ouvrir le dialogue pour ajouter une tâche
            def handle_task_result(result):
                if result:  # L'utilisateur a confirmé
                    task_name = result["name"]
                    task_type = result["type"]
                    
                    # Ajouter la tâche aux créneaux sélectionnés
                    for day, hour in grid.current_selection:
                        grid.add_task_to_schedule(day, hour, task_name, task_type)
                    
                    grid.clear_current_selection()
                    
                    selection_label = self.query_one("#selection-display", Label)
                    selection_label.update(f"✅ Ajouté: {task_name} ({selection_text})")
                else:
                    # Annulé - garder la sélection
                    selection_label = self.query_one("#selection-display", Label)
                    selection_label.update("🔙 Retour - sélection conservée")
            
            # Ouvrir le dialogue modal
            dialog = TaskDialog(selection_text, grid.current_selection.copy())
            self.push_screen(dialog, handle_task_result)
            
        else:
            selection_label = self.query_one("#selection-display", Label)
            selection_label.update("❌ Aucune sélection à confirmer")

def run_interactive_schedule():
    """Lancer l'interface interactive de l'emploi du temps"""
    app = InteractiveScheduleApp()
    app.run()

if __name__ == "__main__":
    run_interactive_schedule()