# PlanIt 🗓️

Terminal-based task scheduler with intelligent planning

## Description

PlanIt est une application terminale légère et interactive conçue pour aider les étudiants (ou tout utilisateur Linux) à organiser efficacement leurs tâches et à planifier automatiquement leur emploi du temps.

## Fonctionnalités

- ✅ Gestion des tâches (ajout, édition, suppression, tri par priorité ou deadline)
- 📅 Définition des créneaux horaires disponibles dans la semaine
- 🤖 Génération automatique d'un planning optimal
- 🎨 Interface terminale agréable et interactive avec Textual
- 📊 Export du planning hebdomadaire sous forme de tableau

## Installation

```bash
git clone <votre-repo>
cd planit
pip install -e .
```

## Utilisation

```bash
# Interface interactive
planit interactive

# Ajouter une tâche
planit task add "Réviser mathématiques" --duration 2 --priority high

# Voir les tâches
planit task list

# Configurer les créneaux
planit schedule add monday 09:00 12:00

# Voir les statistiques
planit stats
```

## Technologies

- Python 3.8+
- Textual (Interface terminale)
- Typer (CLI)
- Rich (Affichage)
- SQLite (Base de données)
- SQLAlchemy (ORM)
- Pydantic (Validation)

## Développement

```bash
pip install -e ".[dev]"
pytest
```

## Licence

MIT
