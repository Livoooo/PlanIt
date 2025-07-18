"""
Setup script for PlanIt - Simple Task Manager
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]
else:
    requirements = ["rich>=13.0.0", "typer>=0.9.0", "textual>=0.44.0"]

setup(
    name="planit-taskmanager",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A lightweight terminal-based task manager and scheduler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/planit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "planit=main:main",
        ],
    },
    keywords="task manager, scheduler, terminal, cli, tui, productivity",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/planit/issues",
        "Source": "https://github.com/yourusername/planit",
    },
)