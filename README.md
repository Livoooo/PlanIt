# 📋 PlanIt - Simple Task Manager
aazdaz
A lightweight terminal-based task manager and scheduler designed for students and developers who prefer working in the terminal.

## ✨ Features

- ✅ **Task Management**: Add, delete, complete, and list tasks
- 📅 **Auto-Scheduling**: Intelligent automatic scheduling based on availability
- 🔄 **Recurring Tasks**: Support for daily/weekly recurring tasks  
- 📊 **Project Timeline**: Visual project timeline with Gantt-style display
- 🖥️ **Multiple Interfaces**: CLI, TUI (Textual), and Interactive modes
- 💾 **SQLite Database**: Local storage with no external dependencies
- 🎨 **Rich Terminal Output**: Beautiful formatting with Rich library

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone git@github.com:Livoooo/PlanIt.git
cd planit

python3 -m venv planit-env
source planit-env/bin/activate  # Linux/Mac
# ou
planit-env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Or install as package
pip install -e .
```

### Basic Usage

```bash
# Launch TUI interface (recommended)
python main.py tui

# Interactive terminal mode
python main.py interactive

# CLI commands
python main.py add "Study Python" --duration 2
python main.py list
python main.py schedule
python main.py planning
```

## 🖥️ Interfaces

### 1. TUI (Textual User Interface) - Recommended
```bash
python main.py tui
```
- Modern terminal GUI with mouse support
- Sidebar navigation with buttons
- Modal dialogs for input
- Real-time updates

### 2. Interactive Mode
```bash
python main.py interactive
```
- Command-prompt style interface
- Step-by-step task creation
- Rich formatted output

### 3. CLI Commands
```bash
# Task management
python main.py add "Task name" --duration 2
python main.py list
python main.py delete 1
python main.py done 1

# Scheduling
python main.py schedule          # Auto-schedule tasks
python main.py planning          # Show weekly view
python main.py planning --next   # Next week
python main.py reset            # Reset schedule

# Projects
python main.py project "Web App" --start 06/01 --end 08/31
python main.py timeline         # Show project timeline
python main.py delproject 1     # Delete project
```

## 📖 Detailed Usage

### Adding Tasks

**Simple Task:**
```bash
python main.py add "Read documentation" --duration 1
```

**Recurring Task:**
```bash
python main.py add "Daily standup" --duration 1 --recurring --days "mon,tue,wed,thu,fri" --start 9
```

**Manual Scheduling:**
```bash
python main.py add "Important meeting" --duration 2 --manual --date "06/15" --start 14
```

### Auto-Scheduling

PlanIt automatically schedules your tasks based on:
- Your availability windows (default: 9h-18h Mon-Fri)
- Existing recurring tasks
- Task duration requirements
- Chronological priority

```bash
python main.py schedule  # Auto-schedule all unscheduled tasks
```

### Project Management

```bash
# Add project
python main.py project "Mobile App" --start 07/01 --end 09/30 --desc "iOS/Android app development"

# View timeline
python main.py timeline

# Delete project
python main.py delproject 1
```

## 🗂️ Project Structure

```
planit/
├── planit/
│   ├── core/           # Business logic
│   │   ├── database.py # SQLite operations
│   │   └── planner.py  # Scheduling engine
│   ├── cli/            # Command line interface
│   │   ├── commands.py # Typer commands
│   │   └── interactive.py # Interactive mode
│   ├── tui/            # Terminal user interface
│   │   ├── app.py      # Main TUI app
│   │   ├── modals.py   # Dialog windows
│   │   └── styles.py   # CSS styling
│   └── utils/          # Shared utilities
│       └── console.py  # Rich console setup
├── main.py             # Entry point
├── requirements.txt    # Dependencies
└── setup.py           # Installation script
```

## 🛠️ Development

### Running Tests
```bash
# Install development dependencies
pip install pytest black flake8

# Run tests (when available)
pytest

# Code formatting
black .

# Linting
flake8 planit/
```

### Database Schema

PlanIt uses SQLite with three main tables:

- **tasks**: Task storage with scheduling info
- **projects**: Project timeline data
- **availability**: User availability windows

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.

## 🆘 Support

- 📧 Email: olivier.pouech@epitech.eu
- 🐛 Issues: [GitHub Issues](https://github.com/Livoooo/planit/issues)
- 📖 Docs: [Wiki](https://github.com/Livoooo/planit/wiki)

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- [Textual](https://github.com/Textualize/textual) - Modern TUI framework
- [Typer](https://github.com/tiangolo/typer) - CLI frameworktest ngrok webhook
test ngrok webhook
dza