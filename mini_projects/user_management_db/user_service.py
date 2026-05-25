"""
user_service.py

Business logic for user management operations.
This is the service layer — it sits between the API and the database.

Pattern:
    API endpoint -> service function -> database query -> return result

This exact pattern is used in every FastAPI + SQLAlchemy project.
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from mini_projects.user_management_db.database import Database


def hash_password(password):
    """Simple password hashing. In production use bcrypt or argon2."""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token():
    """Generate a secure random session token."""
    return secrets.token_hex(32)


class UserService:
    """
    Service layer for all user-related operations.
    Each method maps to one API endpoint.
    """

    def __init__(self):
        self.db = Database()

    def create_user(self, username, email, password, role="user"):
        """Create a new user. Returns user dict or raises ValueError."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")

        password_hash = hash_password(password)

        try:
            with self.db.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, role)
                    VALUES (?, ?, ?, ?)
                """, (username, email, password_hash, role))

                user_id = cursor.lastrowid

                # Log the action
                cursor.execute("""
                    INSERT INTO audit_log (user_id, action, details)
                    VALUES (?, ?, ?)
                """, (user_id, "user_created", f"username={username}"))

            return self.get_user_by_id(user_id)

        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                field = "username" if "username" in str(e) else "email"
                raise ValueError(f"{field} already exists.")
            raise e

    def get_user_by_id(self, user_id):
        """Fetch a single user by ID."""
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT id, username, email, role, active, created_at
                FROM users WHERE id = ?
            """, (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_users(self, active_only=True):
        """Fetch all users, optionally filtering to active only."""
        with self.db.get_cursor() as cursor:
            if active_only:
                cursor.execute("""
                    SELECT id, username, email, role, active, created_at
                    FROM users WHERE active = 1 ORDER BY id
                """)
            else:
                cursor.execute("""
                    SELECT id, username, email, role, active, created_at
                    FROM users ORDER BY id
                """)
            return [dict(row) for row in cursor.fetchall()]

    def update_user_role(self, user_id, new_role, changed_by_id):
        """Update a user role and log the change."""
        valid_roles = ["user", "editor", "admin"]
        if new_role not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")

        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE users SET role = ? WHERE id = ?
            """, (new_role, user_id))

            if cursor.rowcount == 0:
                raise ValueError(f"User {user_id} not found.")

            cursor.execute("""
                INSERT INTO audit_log (user_id, action, details)
                VALUES (?, ?, ?)
            """, (changed_by_id, "role_changed",
                   f"target_user={user_id} new_role={new_role}"))

        return self.get_user_by_id(user_id)

    def deactivate_user(self, user_id):
        """Soft delete — marks user inactive instead of deleting."""
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE users SET active = 0 WHERE id = ?
            """, (user_id,))

            if cursor.rowcount == 0:
                raise ValueError(f"User {user_id} not found.")

            cursor.execute("""
                INSERT INTO audit_log (user_id, action, details)
                VALUES (?, ?, ?)
            """, (user_id, "user_deactivated", f"user_id={user_id}"))

    def get_audit_log(self, limit=10):
        """Fetch recent audit log entries."""
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT a.timestamp, a.action, a.details, u.username
                FROM audit_log a
                LEFT JOIN users u ON a.user_id = u.id
                ORDER BY a.timestamp DESC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]