from pathlib import Path

files = {}

# ── File 1: sql_basics.py ─────────────────────────────────────────

files["fundamentals/databases/__init__.py"] = ""

files["fundamentals/databases/sql_basics.py"] = """
import sqlite3
from pathlib import Path

DB_PATH = Path("fundamentals/databases/basics_demo.db")

print("=== Creating a Database and Table ===")

# connect() creates the file if it does not exist
# Using context manager ensures connection closes cleanly
with sqlite3.connect(DB_PATH) as conn:
    # cursor executes SQL statements
    cursor = conn.cursor()

    # CREATE TABLE IF NOT EXISTS prevents error if table already exists
    cursor.execute(\"\"\"
        CREATE TABLE IF NOT EXISTS servers (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL UNIQUE,
            region      TEXT    NOT NULL,
            status      TEXT    NOT NULL DEFAULT 'stopped',
            cpu_usage   REAL    DEFAULT 0.0,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    \"\"\")

    # conn.commit() saves changes to disk
    # Without commit, changes exist only in memory
    conn.commit()
    print(f"  Database created: {DB_PATH}")
    print(f"  Table 'servers' ready.")


print("\\n=== Inserting Data ===")

servers_to_add = [
    ("api-server-01", "us-east-1",  "running",  45.2),
    ("db-server-01",  "us-east-1",  "running",  78.9),
    ("cache-01",      "us-west-2",  "degraded", 91.3),
    ("api-server-02", "us-west-2",  "stopped",   0.0),
]

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    # executemany inserts multiple rows efficiently
    # ? placeholders prevent SQL injection — ALWAYS use placeholders
    cursor.executemany(\"\"\"
        INSERT OR IGNORE INTO servers (name, region, status, cpu_usage)
        VALUES (?, ?, ?, ?)
    \"\"\", servers_to_add)

    conn.commit()
    print(f"  Inserted {cursor.rowcount} rows.")


print("\\n=== Selecting Data ===")

with sqlite3.connect(DB_PATH) as conn:
    # row_factory makes rows behave like dicts
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Select all rows
    cursor.execute("SELECT * FROM servers ORDER BY id")
    rows = cursor.fetchall()

    print(f"  Total servers: {len(rows)}")
    for row in rows:
        print(f"  [{row['id']}] {row['name']} | {row['region']} | {row['status']}")


print("\\n=== Filtering with WHERE ===")

with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # WHERE filters rows — always use ? for values, never f-strings
    cursor.execute(\"\"\"
        SELECT name, cpu_usage FROM servers
        WHERE cpu_usage > ?
        ORDER BY cpu_usage DESC
    \"\"\", (80.0,))

    high_cpu = cursor.fetchall()
    print(f"  High CPU servers (> 80%):")
    for row in high_cpu:
        print(f"    {row['name']}: {row['cpu_usage']}%")


print("\\n=== Updating Data ===")

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    cursor.execute(\"\"\"
        UPDATE servers SET status = ?, cpu_usage = ?
        WHERE name = ?
    \"\"\", ("running", 32.1, "api-server-02"))

    conn.commit()
    print(f"  Updated {cursor.rowcount} row(s).")


print("\\n=== Aggregation Queries ===")

with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(\"\"\"
        SELECT
            COUNT(*)            AS total,
            AVG(cpu_usage)      AS avg_cpu,
            MAX(cpu_usage)      AS max_cpu,
            MIN(cpu_usage)      AS min_cpu
        FROM servers
        WHERE status = 'running'
    \"\"\")

    stats = cursor.fetchone()
    print(f"  Running servers : {stats['total']}")
    print(f"  Average CPU     : {stats['avg_cpu']:.1f}%")
    print(f"  Max CPU         : {stats['max_cpu']}%")
    print(f"  Min CPU         : {stats['min_cpu']}%")


print("\\n=== Deleting Data ===")

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM servers WHERE status = ?", ("stopped",))
    conn.commit()
    print(f"  Deleted {cursor.rowcount} stopped server(s).")

print("\\nsql_basics.py completed successfully.")
""".strip()

# ── File 2: database_manager.py ───────────────────────────────────

files["fundamentals/databases/database_manager.py"] = """
import sqlite3
from pathlib import Path
from contextlib import contextmanager


DB_PATH = Path("fundamentals/databases/managed_demo.db")


class DatabaseManager:
    \"\"\"
    Professional database manager using context managers.

    Handles connection lifecycle, row factory, and error handling.
    This pattern is the foundation of every ORM (SQLAlchemy, Django ORM).

    Usage:
        db = DatabaseManager("myapp.db")
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users")
    \"\"\"

    def __init__(self, db_path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialise()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # Enable foreign key enforcement
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @contextmanager
    def get_cursor(self):
        \"\"\"
        Context manager that provides a cursor and handles
        commit on success and rollback on error automatically.
        \"\"\"
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _initialise(self):
        with self.get_cursor() as cursor:
            cursor.execute(\"\"\"
                CREATE TABLE IF NOT EXISTS users (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    username   TEXT    NOT NULL UNIQUE,
                    email      TEXT    NOT NULL UNIQUE,
                    role       TEXT    NOT NULL DEFAULT 'viewer',
                    active     INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT    DEFAULT (datetime('now'))
                )
            \"\"\")


# --- Using DatabaseManager ---
print("=== DatabaseManager Pattern ===")

db = DatabaseManager(DB_PATH)
print(f"  Database ready: {DB_PATH}")

# Insert users
print("\\n=== Inserting Users ===")
users = [
    ("alice",   "alice@company.com",   "admin"),
    ("bob",     "bob@company.com",     "editor"),
    ("carol",   "carol@company.com",   "viewer"),
    ("diana",   "diana@company.com",   "editor"),
]

with db.get_cursor() as cursor:
    cursor.executemany(\"\"\"
        INSERT OR IGNORE INTO users (username, email, role)
        VALUES (?, ?, ?)
    \"\"\", users)
    print(f"  Inserted users.")

# Query users
print("\\n=== Querying Users ===")
with db.get_cursor() as cursor:
    cursor.execute("SELECT * FROM users ORDER BY id")
    all_users = cursor.fetchall()
    for user in all_users:
        print(
            f"  [{user['id']}] {user['username']:<10} "
            f"{user['email']:<28} {user['role']}"
        )

# Filter by role
print("\\n=== Editors Only ===")
with db.get_cursor() as cursor:
    cursor.execute(\"\"\"
        SELECT username, email FROM users
        WHERE role = ? AND active = 1
    \"\"\", ("editor",))
    editors = cursor.fetchall()
    for user in editors:
        print(f"  {user['username']}: {user['email']}")

# Update a user
print("\\n=== Updating User Role ===")
with db.get_cursor() as cursor:
    cursor.execute(\"\"\"
        UPDATE users SET role = ? WHERE username = ?
    \"\"\", ("admin", "bob"))
    print(f"  Updated {cursor.rowcount} user(s).")

# Verify update
with db.get_cursor() as cursor:
    cursor.execute("SELECT username, role FROM users WHERE username = ?", ("bob",))
    user = cursor.fetchone()
    print(f"  Bob's new role: {user['role']}")

print("\\ndatabase_manager.py completed successfully.")
""".strip()

# ── Mini project: user_management_db ──────────────────────────────

files["mini_projects/user_management_db/__init__.py"] = ""

files["mini_projects/user_management_db/models.py"] = """
\"\"\"
models.py

Database schema definitions and table creation.
In production this would use SQLAlchemy models.
Today we write raw SQL to understand what ORMs do underneath.
\"\"\"

CREATE_USERS_TABLE = \"\"\"
    CREATE TABLE IF NOT EXISTS users (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        username     TEXT    NOT NULL UNIQUE,
        email        TEXT    NOT NULL UNIQUE,
        password_hash TEXT   NOT NULL,
        role         TEXT    NOT NULL DEFAULT 'user',
        active       INTEGER NOT NULL DEFAULT 1,
        created_at   TEXT    DEFAULT (datetime('now')),
        last_login   TEXT
    )
\"\"\"

CREATE_SESSIONS_TABLE = \"\"\"
    CREATE TABLE IF NOT EXISTS sessions (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        token      TEXT    NOT NULL UNIQUE,
        created_at TEXT    DEFAULT (datetime('now')),
        expires_at TEXT    NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
\"\"\"

CREATE_AUDIT_LOG_TABLE = \"\"\"
    CREATE TABLE IF NOT EXISTS audit_log (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER,
        action     TEXT    NOT NULL,
        details    TEXT,
        timestamp  TEXT    DEFAULT (datetime('now'))
    )
\"\"\"

ALL_TABLES = [
    CREATE_USERS_TABLE,
    CREATE_SESSIONS_TABLE,
    CREATE_AUDIT_LOG_TABLE,
]
""".strip()

files["mini_projects/user_management_db/database.py"] = """
\"\"\"
database.py
Database connection and management for user_management_db.
\"\"\"

import sqlite3
from pathlib import Path
from contextlib import contextmanager
from mini_projects.user_management_db.models import ALL_TABLES

DB_PATH = Path("mini_projects/user_management_db/users.db")


class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialise()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @contextmanager
    def get_cursor(self):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _initialise(self):
        with self.get_cursor() as cursor:
            for table_sql in ALL_TABLES:
                cursor.execute(table_sql)
""".strip()

files["mini_projects/user_management_db/user_service.py"] = """
\"\"\"
user_service.py

Business logic for user management operations.
This is the service layer — it sits between the API and the database.

Pattern:
    API endpoint -> service function -> database query -> return result

This exact pattern is used in every FastAPI + SQLAlchemy project.
\"\"\"

import hashlib
import secrets
from datetime import datetime, timedelta
from mini_projects.user_management_db.database import Database


def hash_password(password):
    \"\"\"Simple password hashing. In production use bcrypt or argon2.\"\"\"
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token():
    \"\"\"Generate a secure random session token.\"\"\"
    return secrets.token_hex(32)


class UserService:
    \"\"\"
    Service layer for all user-related operations.
    Each method maps to one API endpoint.
    \"\"\"

    def __init__(self):
        self.db = Database()

    def create_user(self, username, email, password, role="user"):
        \"\"\"Create a new user. Returns user dict or raises ValueError.\"\"\"
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")

        password_hash = hash_password(password)

        try:
            with self.db.get_cursor() as cursor:
                cursor.execute(\"\"\"
                    INSERT INTO users (username, email, password_hash, role)
                    VALUES (?, ?, ?, ?)
                \"\"\", (username, email, password_hash, role))

                user_id = cursor.lastrowid

                # Log the action
                cursor.execute(\"\"\"
                    INSERT INTO audit_log (user_id, action, details)
                    VALUES (?, ?, ?)
                \"\"\", (user_id, "user_created", f"username={username}"))

            return self.get_user_by_id(user_id)

        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                field = "username" if "username" in str(e) else "email"
                raise ValueError(f"{field} already exists.")
            raise e

    def get_user_by_id(self, user_id):
        \"\"\"Fetch a single user by ID.\"\"\"
        with self.db.get_cursor() as cursor:
            cursor.execute(\"\"\"
                SELECT id, username, email, role, active, created_at
                FROM users WHERE id = ?
            \"\"\", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_users(self, active_only=True):
        \"\"\"Fetch all users, optionally filtering to active only.\"\"\"
        with self.db.get_cursor() as cursor:
            if active_only:
                cursor.execute(\"\"\"
                    SELECT id, username, email, role, active, created_at
                    FROM users WHERE active = 1 ORDER BY id
                \"\"\")
            else:
                cursor.execute(\"\"\"
                    SELECT id, username, email, role, active, created_at
                    FROM users ORDER BY id
                \"\"\")
            return [dict(row) for row in cursor.fetchall()]

    def update_user_role(self, user_id, new_role, changed_by_id):
        \"\"\"Update a user role and log the change.\"\"\"
        valid_roles = ["user", "editor", "admin"]
        if new_role not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")

        with self.db.get_cursor() as cursor:
            cursor.execute(\"\"\"
                UPDATE users SET role = ? WHERE id = ?
            \"\"\", (new_role, user_id))

            if cursor.rowcount == 0:
                raise ValueError(f"User {user_id} not found.")

            cursor.execute(\"\"\"
                INSERT INTO audit_log (user_id, action, details)
                VALUES (?, ?, ?)
            \"\"\", (changed_by_id, "role_changed",
                   f"target_user={user_id} new_role={new_role}"))

        return self.get_user_by_id(user_id)

    def deactivate_user(self, user_id):
        \"\"\"Soft delete — marks user inactive instead of deleting.\"\"\"
        with self.db.get_cursor() as cursor:
            cursor.execute(\"\"\"
                UPDATE users SET active = 0 WHERE id = ?
            \"\"\", (user_id,))

            if cursor.rowcount == 0:
                raise ValueError(f"User {user_id} not found.")

            cursor.execute(\"\"\"
                INSERT INTO audit_log (user_id, action, details)
                VALUES (?, ?, ?)
            \"\"\", (user_id, "user_deactivated", f"user_id={user_id}"))

    def get_audit_log(self, limit=10):
        \"\"\"Fetch recent audit log entries.\"\"\"
        with self.db.get_cursor() as cursor:
            cursor.execute(\"\"\"
                SELECT a.timestamp, a.action, a.details, u.username
                FROM audit_log a
                LEFT JOIN users u ON a.user_id = u.id
                ORDER BY a.timestamp DESC
                LIMIT ?
            \"\"\", (limit,))
            return [dict(row) for row in cursor.fetchall()]
""".strip()

files["mini_projects/user_management_db/main.py"] = """
\"\"\"
main.py

Entry point for the user management system.
Demonstrates all UserService operations with a full report.

Usage:
    python mini_projects/user_management_db/main.py
\"\"\"

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mini_projects.user_management_db.user_service import UserService


def print_user_table(users):
    print(f"  {'ID':<4} {'Username':<12} {'Email':<28} {'Role':<8} {'Active'}")
    print("  " + "-" * 60)
    for user in users:
        active = "Yes" if user["active"] else "No"
        print(
            f"  {user['id']:<4} {user['username']:<12} "
            f"{user['email']:<28} {user['role']:<8} {active}"
        )


def main():
    service = UserService()

    print("=" * 58)
    print("  USER MANAGEMENT SYSTEM")
    print("=" * 58)

    # Create users
    print("\\n-- Creating Users --")
    try:
        alice = service.create_user("alice", "alice@company.com", "securepass1", "admin")
        print(f"  Created: {alice['username']} (id={alice['id']})")

        bob = service.create_user("bob", "bob@company.com", "securepass2")
        print(f"  Created: {bob['username']} (id={bob['id']})")

        carol = service.create_user("carol", "carol@company.com", "securepass3")
        print(f"  Created: {carol['username']} (id={carol['id']})")

        diana = service.create_user("diana", "diana@company.com", "securepass4")
        print(f"  Created: {diana['username']} (id={diana['id']})")

    except ValueError as e:
        print(f"  Note: {e} (already seeded)")

    # Duplicate check
    print("\\n-- Duplicate User Test --")
    try:
        service.create_user("alice", "alice@company.com", "newpass123")
    except ValueError as e:
        print(f"  Caught expected error: {e}")

    # List all users
    print("\\n-- All Active Users --")
    users = service.get_all_users()
    print_user_table(users)

    # Update role
    print("\\n-- Updating Bob to Editor --")
    try:
        updated = service.update_user_role(
            user_id=2,
            new_role="editor",
            changed_by_id=1
        )
        print(f"  Bob's new role: {updated['role']}")
    except ValueError as e:
        print(f"  Error: {e}")

    # Deactivate user
    print("\\n-- Deactivating Carol --")
    try:
        service.deactivate_user(user_id=3)
        print(f"  Carol deactivated.")
    except ValueError as e:
        print(f"  Error: {e}")

    # Show active users only
    print("\\n-- Active Users After Deactivation --")
    active_users = service.get_all_users(active_only=True)
    print_user_table(active_users)

    # Audit log
    print("\\n-- Audit Log --")
    audit = service.get_audit_log(limit=10)
    for entry in audit:
        print(
            f"  [{entry['timestamp']}] "
            f"{entry['action']:<20} "
            f"{entry['details']}"
        )

    print("\\n" + "=" * 58)
    print(f"  Database saved to: mini_projects/user_management_db/users.db")
    print("=" * 58)


if __name__ == "__main__":
    main()
""".strip()

# ── Write all files ───────────────────────────────────────────────

for filepath, content in files.items():
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Created: {filepath}")

print("\nAll Day 10 files created successfully.")