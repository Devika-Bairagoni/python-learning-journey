"""
database.py
Database connection and management for user_management_db.
"""

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