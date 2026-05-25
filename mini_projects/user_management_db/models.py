"""
models.py

Database schema definitions and table creation.
In production this would use SQLAlchemy models.
Today we write raw SQL to understand what ORMs do underneath.
"""

CREATE_USERS_TABLE = """
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
"""

CREATE_SESSIONS_TABLE = """
    CREATE TABLE IF NOT EXISTS sessions (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER NOT NULL,
        token      TEXT    NOT NULL UNIQUE,
        created_at TEXT    DEFAULT (datetime('now')),
        expires_at TEXT    NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
"""

CREATE_AUDIT_LOG_TABLE = """
    CREATE TABLE IF NOT EXISTS audit_log (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER,
        action     TEXT    NOT NULL,
        details    TEXT,
        timestamp  TEXT    DEFAULT (datetime('now'))
    )
"""

ALL_TABLES = [
    CREATE_USERS_TABLE,
    CREATE_SESSIONS_TABLE,
    CREATE_AUDIT_LOG_TABLE,
]