## Why

Users need to know when tasks are due, not just what to do. Adding optional due dates helps prioritize work, spot overdue items, and plan ahead without leaving the simple todo list workflow.

## What Changes

- Add an optional `due_date` field on each todo (stored in SQLite)
- Extend the add-task form with an optional date picker
- Show due date on each todo item in the list
- Visually distinguish overdue active todos from upcoming ones
- Sort active todos by due date (soonest first; items without a due date last)
- Migrate existing database rows with a nullable `due_date` column (no **BREAKING** API changes for existing routes)

## Capabilities

### New Capabilities

- `todo-due-date`: Optional due dates on todos—capture on create, persist, display, overdue styling, and sort order for active items

### Modified Capabilities

<!-- None — no prior OpenSpec capabilities exist for this project -->

## Impact

- `app.py`: schema migration, queries, add route
- `templates/index.html`: date input on add form, due date display per item
- `static/style.css`: due date and overdue visual styles
- `todos.db`: new nullable `due_date` column on `todos` table
