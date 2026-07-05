"""SQLite database setup and operations."""

import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database.db"


def get_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_type TEXT NOT NULL,
            uploaded_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            upload_id INTEGER,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            file_path TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (upload_id) REFERENCES uploads (id)
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            user_id INTEGER PRIMARY KEY,
            theme TEXT DEFAULT 'light',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )

    conn.commit()
    conn.close()


def create_user(username, email, password_hash, full_name=""):
    """Insert a new user. Returns user id or None if duplicate."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, full_name, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (username, email, password_hash, full_name, datetime.now().isoformat()),
        )
        user_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO settings (user_id, theme) VALUES (?, 'light')",
            (user_id,),
        )
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def get_user_by_username(username):
    """Fetch user record by username."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    """Fetch user record by id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_user_profile(user_id, full_name, email):
    """Update user profile fields."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET full_name = ?, email = ? WHERE id = ?",
            (full_name, email, user_id),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def save_upload(user_id, filename, file_path, file_type):
    """Record an uploaded file."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO uploads (user_id, filename, file_path, file_type, uploaded_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, filename, file_path, file_type, datetime.now().isoformat()),
    )
    upload_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return upload_id


def get_user_uploads(user_id):
    """Return all uploads for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM uploads WHERE user_id = ? ORDER BY uploaded_at DESC",
        (user_id,),
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_upload_by_id(upload_id, user_id):
    """Return a single upload if it belongs to the user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM uploads WHERE id = ? AND user_id = ?",
        (upload_id, user_id),
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def save_report(user_id, upload_id, title, summary, file_path):
    """Save a generated report."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO reports (user_id, upload_id, title, summary, file_path, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, upload_id, title, summary, file_path, datetime.now().isoformat()),
    )
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id


def get_user_reports(user_id):
    """Return all reports for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM reports WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def get_user_theme(user_id):
    """Return user's theme preference."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT theme FROM settings WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row["theme"] if row else "light"


def set_user_theme(user_id, theme):
    """Update user's theme preference."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE settings SET theme = ? WHERE user_id = ?",
        (theme, user_id),
    )
    conn.commit()
    conn.close()


def get_dashboard_stats(user_id):
    """Return summary stats for the dashboard."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS c FROM uploads WHERE user_id = ?", (user_id,))
    uploads_count = cursor.fetchone()["c"]
    cursor.execute("SELECT COUNT(*) AS c FROM reports WHERE user_id = ?", (user_id,))
    reports_count = cursor.fetchone()["c"]
    conn.close()
    return {"uploads": uploads_count, "reports": reports_count}
