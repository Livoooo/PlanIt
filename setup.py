#!/usr/bin/env python3
"""
Setup configuration for PlanIt
"""

from setuptools import setup, find_packages

# Lire le README pour la description longue
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "PlanIt - Terminal Task Scheduler"

# Lire les requirements
try:
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
except FileNotFoundError:
    requirements = [
        "textual>=0.44.0",
        "typer>=0.9.0",
        "rich>=13.0.0",
        "sqlalchemy>=2.0.0",
        "python-dateutil>=2.8.0",
        "pydantic>=2.0.0"
    ]

setup(
    name="planit",
    version="0.1.0",
    author="Livo",  # À remplacer par ton nom
    author_email="olivier.pouech@epitech.eu",  # À remplacer par ton email
    description="Terminal-based task scheduler with intelligent planning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/planit",  # À remplacer par ton repo GitHub
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "planit=planit.main:app",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="task scheduler planning terminal cli productivity",
    project_urls={
        "Bug Reports": "https://github.com/username/planit/issues",
        "Source": "https://github.com/username/planit",
        "Documentation": "https://github.com/username/planit/blob/main/README.md",
    },
)