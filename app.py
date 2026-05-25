import re
import sqlite3
from datetime import date, datetime
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__)
DATABASE = Path(__file__).parent / "todos.db"
DATE_FMT = "%Y-%m-%d"
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def _ensure_due_date_column(conn):
    columns = {
        row[1] for row in conn.execute("PRAGMA table_info(todos)").fetchall()
    }
    if "due_date" not in columns:
        conn.execute("ALTER TABLE todos ADD COLUMN due_date TEXT")


def parse_due_date(value):
    if not value or not str(value).strip():
        return None
    value = str(value).strip()
    if not DATE_PATTERN.match(value):
        return None
    try:
        datetime.strptime(value, DATE_FMT).date()
    except ValueError:
        return None
    return value


def format_due_date(value):
    if not value:
        return None
    try:
        d = datetime.strptime(value, DATE_FMT).date()
    except ValueError:
        return None
    return f"{d.strftime('%b')} {d.day}, {d.year}"


def is_overdue(due_date, done):
    if done or not due_date:
        return False
    try:
        d = datetime.strptime(due_date, DATE_FMT).date()
    except ValueError:
        return False
    return d < date.today()


def enrich_todo(row):
    todo = dict(row)
    todo["due_date_display"] = format_due_date(todo.get("due_date"))
    todo["is_overdue"] = is_overdue(todo.get("due_date"), todo.get("done"))
    return todo


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )
        _ensure_due_date_column(conn)


@app.route("/")
def index():
    db = get_db()
    rows = db.execute(
        """
        SELECT id, text, done, due_date, created_at
        FROM todos
        ORDER BY done ASC,
          CASE
            WHEN done = 0 AND due_date IS NULL THEN 1
            WHEN done = 0 THEN 0
            ELSE 2
          END,
          due_date ASC,
          created_at DESC
        """
    ).fetchall()
    todos = [enrich_todo(row) for row in rows]
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "").strip()
    if text:
        due_date = parse_due_date(request.form.get("due_date", ""))
        db = get_db()
        db.execute(
            "INSERT INTO todos (text, due_date) VALUES (?, ?)",
            (text, due_date),
        )
        db.commit()
    return redirect(url_for("index"))


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id):
    db = get_db()
    db.execute(
        "UPDATE todos SET done = CASE WHEN done = 1 THEN 0 ELSE 1 END WHERE id = ?",
        (todo_id,),
    )
    db.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    db = get_db()
    db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db.commit()
    return redirect(url_for("index"))


@app.route("/clear-completed", methods=["POST"])
def clear_completed():
    db = get_db()
    db.execute("DELETE FROM todos WHERE done = 1")
    db.commit()
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
