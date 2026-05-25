## Context

The app is a Flask + SQLite todo list with server-rendered HTML. Todos have `id`, `text`, `done`, and `created_at`. There is no due date today; `init_db()` only creates the base schema. The UI uses Jinja2 templates, CSS variables (including light/dark themes), and form POST routes for all mutations.

## Goals / Non-Goals

**Goals:**

- Store an optional due date per todo as an ISO date string (`YYYY-MM-DD`)
- Let users set a due date when adding a task (optional `<input type="date">`)
- Display due date on list items; highlight overdue active todos
- Order active todos: earliest due date first, then no-due-date items by `created_at` desc

**Non-Goals:**

- Editing due date on existing todos (future change)
- Time-of-day or timezone-aware deadlines
- Reminders, notifications, or calendar integration
- Filtering views (e.g. "due this week") beyond sort order

## Decisions

### 1. Column type: `TEXT` nullable `due_date`

Store `YYYY-MM-DD` in SQLite as `TEXT` (nullable). Matches HTML `date` input, simple comparisons with `date('now')` in SQL, and no timezone complexity.

**Alternative:** `INTEGER` Unix timestamp — rejected; overkill for date-only.

### 2. Schema migration in `init_db()`

After `CREATE TABLE IF NOT EXISTS`, run `ALTER TABLE todos ADD COLUMN due_date TEXT` inside try/except (or check `PRAGMA table_info`) so existing `todos.db` files upgrade in place without a separate migration tool.

**Alternative:** Drop and recreate table — rejected; loses user data.

### 3. Add form: optional date field only on create

Single add form gets `name="due_date"` optional input. Empty submission stores `NULL`. No new routes for MVP.

### 4. Sort in SQL on index query

Active/completed split stays (`done ASC`). Within active: `ORDER BY CASE WHEN due_date IS NULL THEN 1 ELSE 0 END, due_date ASC, created_at DESC`. Completed: keep `created_at DESC`.

**Alternative:** Sort in Python — rejected; SQL is clearer and matches existing pattern.

### 5. Overdue styling via template + CSS class

Pass `due_date` to template; add class `overdue` when `due_date` is set, todo is not done, and `due_date < today` (compare in Python before render or via Jinja filter). Use `--danger` muted styling consistent with existing theme variables.

### 6. Display format

Show human-readable short date in list (e.g. `May 30, 2026`) via Jinja/`strftime` or a small helper in `app.py` to keep template thin.

## Risks / Trade-offs

- **[Risk] `ALTER TABLE` fails on fresh DB that already has column** → Mitigation: catch duplicate column error or check schema before alter
- **[Risk] Invalid date from tampered POST** → Mitigation: validate `YYYY-MM-DD` in `add()`; ignore invalid values (store NULL)
- **[Risk] Locale/date display inconsistency** → Mitigation: fixed `en-US` style format in template for now; documented as non-goal for i18n
- **[Trade-off] No edit due date** → Users must delete/recreate; acceptable for v1 per non-goals

## Migration Plan

1. Deploy code with `init_db()` migration — existing rows get `due_date = NULL`
2. No manual steps; restart Flask app
3. Rollback: revert code; column can remain unused (harmless) or restore DB backup if needed

## Open Questions

- None blocking implementation. Optional follow-up: inline due-date edit on existing todos.
