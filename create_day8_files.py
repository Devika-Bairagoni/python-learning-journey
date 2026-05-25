from pathlib import Path

files = {}

# ── Package: backend_utils ────────────────────────────────────────

files["backend_utils/__init__.py"] = """
\"\"\"
backend_utils
A reusable internal utilities package for backend engineering.

Exposes the most commonly used utilities at the package level
so callers can import directly from backend_utils instead of
navigating deep module paths.

Usage:
    from backend_utils import Logger, format_response, validate_port
\"\"\"

from backend_utils.logger import Logger
from backend_utils.validators import validate_port, validate_email, validate_environment
from backend_utils.formatters import format_response, format_error
from backend_utils.config import AppConfig

__version__ = "1.0.0"
__author__  = "Your Name"

__all__ = [
    "Logger",
    "validate_port",
    "validate_email",
    "validate_environment",
    "format_response",
    "format_error",
    "AppConfig",
]
""".strip()

files["backend_utils/logger.py"] = """
\"\"\"
backend_utils.logger

Structured logger for backend applications.
Wraps Python logging with consistent formatting and log levels.
\"\"\"

import logging
from datetime import datetime
from pathlib import Path


class Logger:
    \"\"\"
    Structured application logger.
    Creates consistent log format across all modules.

    Usage:
        log = Logger("api_service")
        log.info("Server started on port 8000")
        log.error("Database connection failed")
    \"\"\"

    LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, name, log_file=None, level=logging.DEBUG):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)

        # Prevent duplicate handlers if logger already exists
        if self._logger.handlers:
            return

        # Console handler
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter(self.LOG_FORMAT, self.DATE_FORMAT))
        self._logger.addHandler(console)

        # File handler (optional)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_path, encoding="utf-8")
            file_handler.setFormatter(
                logging.Formatter(self.LOG_FORMAT, self.DATE_FORMAT)
            )
            self._logger.addHandler(file_handler)

    def info(self, message):
        self._logger.info(message)

    def warning(self, message):
        self._logger.warning(message)

    def error(self, message):
        self._logger.error(message)

    def debug(self, message):
        self._logger.debug(message)

    def critical(self, message):
        self._logger.critical(message)
""".strip()

files["backend_utils/validators.py"] = """
\"\"\"
backend_utils.validators

Input validation functions used across backend services.
All validators return the validated value or raise ValueError.
\"\"\"

import re

VALID_ENVIRONMENTS = ["development", "staging", "production"]


def validate_port(port):
    \"\"\"
    Validate a network port number.
    Returns port as int if valid, raises ValueError if not.
    \"\"\"
    try:
        port = int(port)
    except (TypeError, ValueError):
        raise ValueError(f"Port must be a number, got: {port!r}")

    if not (1 <= port <= 65535):
        raise ValueError(f"Port must be between 1 and 65535, got: {port}")

    return port


def validate_email(email):
    \"\"\"
    Validate email address format using regex.
    Returns email if valid, raises ValueError if not.
    \"\"\"
    if not isinstance(email, str):
        raise ValueError(f"Email must be a string, got {type(email).__name__}")

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValueError(f"Invalid email format: {email!r}")

    return email.lower().strip()


def validate_environment(environment):
    \"\"\"
    Validate deployment environment string.
    Returns environment if valid, raises ValueError if not.
    \"\"\"
    if environment not in VALID_ENVIRONMENTS:
        raise ValueError(
            f"Environment must be one of {VALID_ENVIRONMENTS}, "
            f"got: {environment!r}"
        )
    return environment
""".strip()

files["backend_utils/formatters.py"] = """
\"\"\"
backend_utils.formatters

Response formatting utilities for API endpoints.
Ensures consistent JSON response shape across all endpoints.

Standard response shape used by all APIs in this project:
    {
        "success": true/false,
        "data": {...} or null,
        "error": null or "error message",
        "timestamp": "2024-01-15T09:00:00"
    }
\"\"\"

from datetime import datetime


def format_response(data, message=None):
    \"\"\"
    Format a successful API response.

    Args:
        data: The response payload (dict, list, or scalar)
        message: Optional human-readable message

    Returns:
        dict: Standardised success response
    \"\"\"
    response = {
        "success":   True,
        "data":      data,
        "error":     None,
        "timestamp": datetime.utcnow().isoformat(),
    }
    if message:
        response["message"] = message
    return response


def format_error(error_message, error_code=None):
    \"\"\"
    Format a failed API response.

    Args:
        error_message: Human-readable error description
        error_code: Optional machine-readable error code

    Returns:
        dict: Standardised error response
    \"\"\"
    response = {
        "success":   False,
        "data":      None,
        "error":     error_message,
        "timestamp": datetime.utcnow().isoformat(),
    }
    if error_code:
        response["error_code"] = error_code
    return response
""".strip()

files["backend_utils/config.py"] = """
\"\"\"
backend_utils.config

Application configuration class.
Loads config from a dict (or JSON file) and exposes
typed properties with validation.
\"\"\"

from backend_utils.validators import validate_port, validate_environment


class AppConfig:
    \"\"\"
    Typed application configuration with validation.

    Usage:
        config = AppConfig({
            "host": "localhost",
            "port": 8000,
            "environment": "development",
            "debug": True,
        })
        print(config.port)        # 8000
        print(config.is_debug)    # True
    \"\"\"

    DEFAULTS = {
        "host":        "localhost",
        "port":        8000,
        "environment": "development",
        "debug":       False,
        "workers":     1,
    }

    def __init__(self, config_dict=None):
        raw = {**self.DEFAULTS, **(config_dict or {})}

        self._host        = raw["host"]
        self._port        = validate_port(raw["port"])
        self._environment = validate_environment(raw["environment"])
        self._debug       = bool(raw["debug"])
        self._workers     = int(raw["workers"])

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def environment(self):
        return self._environment

    @property
    def is_debug(self):
        return self._debug

    @property
    def workers(self):
        return self._workers

    @property
    def is_production(self):
        return self._environment == "production"

    def __str__(self):
        return (
            f"AppConfig | {self._host}:{self._port} | "
            f"{self._environment} | debug={self._debug}"
        )

    def __repr__(self):
        return (
            f"AppConfig(host={self._host!r}, port={self._port}, "
            f"environment={self._environment!r})"
        )
""".strip()

# ── Mini project: api_simulator ───────────────────────────────────

files["mini_projects/api_simulator/__init__.py"] = ""

files["mini_projects/api_simulator/api_simulator.py"] = """
\"\"\"
api_simulator.py

Simulates a backend API service using the backend_utils package.
Demonstrates how a real service would use an internal utilities package
for logging, validation, config, and response formatting.

Real-world relevance:
    This is the exact pattern used before FastAPI is introduced.
    Every component here maps directly to a FastAPI concept:
    - AppConfig    -> FastAPI Settings (pydantic BaseSettings)
    - format_response -> JSONResponse
    - Logger       -> structlog or Python logging in production
    - validators   -> Pydantic field validators

Usage:
    python mini_projects/api_simulator/api_simulator.py
\"\"\"

import sys
import json
from pathlib import Path

# Add project root to path so backend_utils can be found
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend_utils import (
    Logger,
    AppConfig,
    format_response,
    format_error,
    validate_email,
    validate_port,
)


# Initialise shared logger and config
log    = Logger("api_simulator", log_file="mini_projects/api_simulator/api.log")
config = AppConfig({
    "host":        "0.0.0.0",
    "port":        8000,
    "environment": "development",
    "debug":       True,
    "workers":     2,
})

# In-memory user store (simulates a database table)
USER_DB = {}
NEXT_ID = 1


def create_user(name, email):
    \"\"\"
    Simulate POST /api/users

    Validates input, creates user record, returns formatted response.
    \"\"\"
    global NEXT_ID
    log.info(f"Creating user: name={name!r} email={email!r}")

    try:
        validated_email = validate_email(email)
    except ValueError as e:
        log.error(f"User creation failed: {e}")
        return format_error(str(e), error_code="INVALID_EMAIL")

    # Check for duplicate email
    for user in USER_DB.values():
        if user["email"] == validated_email:
            log.warning(f"Duplicate email attempt: {validated_email}")
            return format_error(
                f"Email already registered: {validated_email}",
                error_code="DUPLICATE_EMAIL"
            )

    user = {
        "id":    NEXT_ID,
        "name":  name.strip(),
        "email": validated_email,
        "active": True,
    }
    USER_DB[NEXT_ID] = user
    NEXT_ID += 1

    log.info(f"User created: id={user['id']} email={user['email']}")
    return format_response(user, message="User created successfully")


def get_user(user_id):
    \"\"\"Simulate GET /api/users/{id}\"\"\"
    log.info(f"Fetching user: id={user_id}")

    user = USER_DB.get(user_id)
    if not user:
        log.warning(f"User not found: id={user_id}")
        return format_error(f"User {user_id} not found", error_code="NOT_FOUND")

    return format_response(user)


def list_users():
    \"\"\"Simulate GET /api/users\"\"\"
    log.info(f"Listing all users. Total: {len(USER_DB)}")
    users = list(USER_DB.values())
    return format_response(users, message=f"{len(users)} users found")


def delete_user(user_id):
    \"\"\"Simulate DELETE /api/users/{id}\"\"\"
    log.info(f"Deleting user: id={user_id}")

    if user_id not in USER_DB:
        return format_error(f"User {user_id} not found", error_code="NOT_FOUND")

    deleted = USER_DB.pop(user_id)
    log.info(f"User deleted: id={user_id}")
    return format_response(
        {"deleted_id": user_id, "name": deleted["name"]},
        message="User deleted successfully"
    )


def print_response(response):
    \"\"\"Pretty print a response dict.\"\"\"
    print(json.dumps(response, indent=2))
    print()


if __name__ == "__main__":
    print("=" * 55)
    print(f"  API SIMULATOR STARTING")
    print(f"  Config : {config}")
    print("=" * 55)
    print()

    log.info("API simulator started")

    # Test 1: Create valid users
    print("-- POST /api/users (valid) --")
    print_response(create_user("Alice Johnson", "alice@company.com"))
    print_response(create_user("Bob Smith", "bob@company.com"))
    print_response(create_user("Carol White", "carol@company.com"))

    # Test 2: Duplicate email
    print("-- POST /api/users (duplicate email) --")
    print_response(create_user("Alice Again", "alice@company.com"))

    # Test 3: Invalid email
    print("-- POST /api/users (invalid email) --")
    print_response(create_user("Dave", "not-an-email"))

    # Test 4: List all users
    print("-- GET /api/users --")
    print_response(list_users())

    # Test 5: Get specific user
    print("-- GET /api/users/1 --")
    print_response(get_user(1))

    # Test 6: Get missing user
    print("-- GET /api/users/999 --")
    print_response(get_user(999))

    # Test 7: Delete user
    print("-- DELETE /api/users/2 --")
    print_response(delete_user(2))

    # Test 8: List after delete
    print("-- GET /api/users (after delete) --")
    print_response(list_users())

    log.info("API simulator completed")
    print(f"\\nLog file written to: mini_projects/api_simulator/api.log")
""".strip()

# ── Write all files ───────────────────────────────────────────────

for filepath, content in files.items():
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Created: {filepath}")

print("\nAll Day 8 files created successfully.")