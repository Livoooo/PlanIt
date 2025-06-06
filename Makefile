# Makefile pour PlanIt

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
