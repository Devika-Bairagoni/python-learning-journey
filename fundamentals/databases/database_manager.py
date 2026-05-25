import sqlite3
from pathlib import Path
from contextlib import contextmanager


DB_PATH = Path("fundamentals/databases/managed_demo.db")


class DatabaseManager:
    """
    Professional database manager using context managers.

    Handles connection lifecycle, row factory, and error handling.
    This pattern is the foundation of every ORM (SQLAlchemy, Django ORM).

    Usage:
        db = DatabaseManager("myapp.db")
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users")
    """

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
        """
        Context manager that provides a cursor and handles
        commit on success and rollback on error automatically.
        """
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
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    username   TEXT    NOT NULL UNIQUE,
                    email      TEXT    NOT NULL UNIQUE,
                    role       TEXT    NOT NULL DEFAULT 'viewer',
                    active     INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT    DEFAULT (datetime('now'))
                )
            """)


# --- Using DatabaseManager ---
print("=== DatabaseManager Pattern ===")

db = DatabaseManager(DB_PATH)
print(f"  Database ready: {DB_PATH}")

# Insert users
print("\n=== Inserting Users ===")
users = [
    ("alice",   "alice@company.com",   "admin"),
    ("bob",     "bob@company.com",     "editor"),
    ("carol",   "carol@company.com",   "viewer"),
    ("diana",   "diana@company.com",   "editor"),
]

with db.get_cursor() as cursor:
    cursor.executemany("""
        INSERT OR IGNORE INTO users (username, email, role)
        VALUES (?, ?, ?)
    """, users)
    print(f"  Inserted users.")

# Query users
print("\n=== Querying Users ===")
with db.get_cursor() as cursor:
    cursor.execute("SELECT * FROM users ORDER BY id")
    all_users = cursor.fetchall()
    for user in all_users:
        print(
            f"  [{user['id']}] {user['username']:<10} "
            f"{user['email']:<28} {user['role']}"
        )

# Filter by role
print("\n=== Editors Only ===")
with db.get_cursor() as cursor:
    cursor.execute("""
        SELECT username, email FROM users
        WHERE role = ? AND active = 1
    """, ("editor",))
    editors = cursor.fetchall()
    for user in editors:
        print(f"  {user['username']}: {user['email']}")

# Update a user
print("\n=== Updating User Role ===")
with db.get_cursor() as cursor:
    cursor.execute("""
        UPDATE users SET role = ? WHERE username = ?
    """, ("admin", "bob"))
    print(f"  Updated {cursor.rowcount} user(s).")

# Verify update
with db.get_cursor() as cursor:
    cursor.execute("SELECT username, role FROM users WHERE username = ?", ("bob",))
    user = cursor.fetchone()
    print(f"  Bob's new role: {user['role']}")

print("\ndatabase_manager.py completed successfully.")