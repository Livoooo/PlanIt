"""
Textual CSS styles for PlanIt TUI
"""

TUI_CSS = """
.container {
    layout: grid;
    grid-size: 2 1;
    grid-gutter: 1;
}

.sidebar {
    background: $surface;
    border: solid $primary;
    width: 25;
}

.main-content {
    background: $surface;
    border: solid $secondary;
    overflow-y: auto;
    padding: 1;
}

.task-table {
    height: 1fr;
}

.button-group {
    layout: horizontal;
    height: 3;
    align: center middle;
}

Button {
    margin: 0 0 1 0;
    width: 100%;
}

#content {
    height: 1fr;
    overflow-y: auto;
    scrollbar-gutter: stable;
}

/* Modal styles */
AddTaskModal {
    align: center middle;
}

AddTaskModal #dialog {
    width: 50;
    height: 15;
    border: thick $background 80%;
    background: $surface;
}

DeleteTaskModal {
    align: center middle;
}

DeleteTaskModal #dialog {
    width: 40;
    height: 12;
    border: thick $background 80%;
    background: $surface;
}

AddProjectModal {
    align: center middle;
}

AddProjectModal #dialog {
    width: 60;
    height: 20;
    border: thick $background 80%;
    background: $surface;
}

MarkDoneModal {
    align: center middle;
}

MarkDoneModal #dialog {
    width: 40;
    height: 12;
    border: thick $background 80%;
    background: $surface;
}
"""