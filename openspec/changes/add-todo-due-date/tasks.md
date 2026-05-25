## 1. Database

- [x] 1.1 Add nullable `due_date TEXT` column migration in `init_db()` (safe for existing DBs)
- [x] 1.2 Update `index` query to `SELECT id, text, done, due_date` with new sort order for active todos
- [x] 1.3 Update `add` route to accept optional `due_date`, validate `YYYY-MM-DD`, store NULL when empty/invalid

## 2. Backend helpers

- [x] 2.1 Add helper to format due date for display (e.g. `May 30, 2026`)
- [x] 2.2 Add helper or template context to detect overdue active todos (`due_date < today`)

## 3. UI — add form

- [x] 3.1 Add optional `<input type="date" name="due_date">` to add form in `templates/index.html`
- [x] 3.2 Style date input in `static/style.css` to match existing form controls (light/dark themes)

## 4. UI — todo list

- [x] 4.1 Show due date label on items that have `due_date`
- [x] 4.2 Apply `overdue` class to active todos past due date
- [x] 4.3 Add CSS for `.due-date` and `.todo-item.overdue` using existing theme variables

## 5. Verification

- [x] 5.1 Manually test: add with/without due date, overdue styling, sort order, existing DB migration
- [x] 5.2 Confirm completed todos are never marked overdue
