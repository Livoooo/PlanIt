import pytest
from planit.models.task import Task, Priority, TaskStatus

def test_task_creation():
    """Test basique de création de tâche"""
    # Ce test sera étendu quand on aura la base de données
    assert Priority.HIGH.value == "high"
    assert TaskStatus.TODO.value == "todo"
