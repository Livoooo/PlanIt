#!/usr/bin/env python3
"""
PlanIt - Terminal Task Scheduler
Point d'entrée principal de l'application
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime, timedelta

# Configuration de l'application Typer
app = typer.Typer(
    name="planit",
    help="🗓️ PlanIt - Terminal Task Scheduler",
    add_completion=False
)

console = Console()

@app.callback()
def main():
    """
    PlanIt - Organisez vos tâches efficacement dans le terminal
    """
    pass

@app.command()
def interactive():
    """Lance l'interface interactive pour gérer l'emploi du temps"""
    console.print("🚀 [bold blue]Lancement de l'interface interactive...[/bold blue]")
    console.print("📱 Utilisez la souris pour cliquer et glisser sur les créneaux")
    console.print("💡 Appuyez sur 'q' pour quitter\n")
    
    try:
        from .ui.schedule_widget import run_interactive_schedule
        run_interactive_schedule()
    except ImportError:
        console.print("❌ [red]Interface interactive non disponible[/red]")
        console.print("💡 Installez les dépendances: pip install textual")
    except Exception as e:
        console.print(f"❌ [red]Erreur: {e}[/red]")
    """Commande de test pour vérifier que tout fonctionne"""
    console.print("🎉 [bold green]PlanIt fonctionne ![/bold green]")
    console.print("📋 Gestionnaire de tâches dans le terminal")
    console.print("🚀 Prêt pour le développement !")

@app.command()
def version():
    """Affiche la version de PlanIt"""
    console.print("PlanIt v0.1.0")

@app.command()
def edt():
    """Affiche l'emploi du temps de la semaine"""
    console.print(Panel.fit("📅 [bold blue]Emploi du temps - Semaine courante[/bold blue]"))
    
    # Créer le tableau de l'emploi du temps
    table = Table(title="Semaine du " + datetime.now().strftime("%d/%m/%Y"))
    
    # Ajouter les colonnes (jours de la semaine)
    table.add_column("Heure", style="cyan", no_wrap=True)
    table.add_column("Lundi", style="green")
    table.add_column("Mardi", style="green") 
    table.add_column("Mercredi", style="green")
    table.add_column("Jeudi", style="green")
    table.add_column("Vendredi", style="green")
    table.add_column("Samedi", style="yellow")
    table.add_column("Dimanche", style="yellow")
    
    # Générer les créneaux horaires (de 8h à 20h par exemple)
    start_hour = 8
    end_hour = 20
    
    for hour in range(start_hour, end_hour):
        time_slot = f"{hour:02d}:00-{hour+1:02d}:00"
        
        # Pour l'instant, on met des cases vides ou des exemples
        # Plus tard, on récupérera les vraies données de la base
        row_data = [time_slot]
        
        # Exemple de données fictives pour montrer le rendu
        if hour == 9:
            row_data.extend(["Mathématiques", "", "Physique", "", "", "", ""])
        elif hour == 14:
            row_data.extend(["", "Programmation", "", "Anglais", "", "", ""])
        elif hour == 16:
            row_data.extend(["", "", "Projet PlanIt", "", "Sport", "", ""])
        else:
            row_data.extend(["", "", "", "", "", "", ""])
        
        table.add_row(*row_data)
    
    console.print(table)
    
    # Afficher des infos supplémentaires
    console.print("\n📊 [bold]Résumé de la semaine[/bold]")
    console.print("• Tâches programmées: [green]3[/green]")
    console.print("• Heures libres: [yellow]45h[/yellow]") 
    console.print("• Heures occupées: [red]3h[/red]")
    console.print("\n💡 [dim]Utilisez 'planit task add' pour ajouter des tâches[/dim]")

if __name__ == "__main__":
    app()