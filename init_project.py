#!/usr/bin/env python3
"""
Script pour initialiser la structure complète du projet PlanIt
Exécute ce script pour créer tous les dossiers et fichiers de base
"""

import os
from pathlib import Path

def create_project_structure():
    """Crée la structure complète du projet PlanIt"""
    
    # Structure des dossiers à créer
    directories = [
        "planit",
        "planit/cli",
        "planit/models", 
        "planit/core",
        "planit/ui",
        "planit/utils",
        "tests",
        "docs",
        "examples"
    ]
    
    # Fichiers à créer avec leur contenu de base
    files = {
        # Fichiers __init__.py
        "planit/__init__.py": '"""PlanIt - Terminal Task Scheduler"""\n__version__ = "0.1.0"\n',
        "planit/cli/__init__.py": "",
        "planit/models/__init__.py": "",
        "planit/core/__init__.py": "",
        "planit/ui/__init__.py": "",
        "planit/utils/__init__.py": "",
        "tests/__init__.py": "",
        
        # README.md
        "README.md": """# PlanIt 🗓️

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
""",
        
        # .gitignore
        ".gitignore": """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# PlanIt specific
.planit/
*.db
""",
        
        # Fichier de configuration de développement
        "pyproject.toml": """[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ['py38']
include = '\\.pyi?$'

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
""",
        
        # Fichier de test exemple
        "tests/test_basic.py": """import pytest
from planit.models.task import Task, Priority, TaskStatus

def test_task_creation():
    \"\"\"Test basique de création de tâche\"\"\"
    # Ce test sera étendu quand on aura la base de données
    assert Priority.HIGH.value == "high"
    assert TaskStatus.TODO.value == "todo"
""",
        
        # Makefile pour les tâches courantes
        "Makefile": """# Makefile pour PlanIt

.PHONY: install dev test clean format lint run

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=planit --cov-report=html

format:
	black planit/ tests/

lint:
	flake8 planit/ tests/
	mypy planit/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

run:
	python -m planit

help:
	@echo "Commandes disponibles:"
	@echo "  install     - Installer le package"
	@echo "  dev         - Installer en mode développement"
	@echo "  test        - Lancer les tests"
	@echo "  test-cov    - Tests avec coverage"
	@echo "  format      - Formater le code avec black"
	@echo "  lint        - Analyser le code"
	@echo "  clean       - Nettoyer les fichiers temporaires"
	@echo "  run         - Lancer l'application"
""",
    }
    
    # Créer les dossiers
    print("📁 Création de la structure des dossiers...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}/")
    
    # Créer les fichiers
    print("\n📄 Création des fichiers de base...")
    for file_path, content in files.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ {file_path}")
    
    print(f"\n🎉 Structure du projet créée avec succès!")
    print(f"📍 Répertoire: {Path.cwd()}")
    
    print(f"\n🚀 Prochaines étapes:")
    print(f"   1. cd dans le répertoire du projet")
    print(f"   2. python init_project.py  (ce script)")
    print(f"   3. pip install -e .")
    print(f"   4. Commencer le développement!")

if __name__ == "__main__":
    create_project_structure()