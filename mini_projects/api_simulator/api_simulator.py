"""
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
"""

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
    """
    Simulate POST /api/users

    Validates input, creates user record, returns formatted response.
    """
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
    """Simulate GET /api/users/{id}"""
    log.info(f"Fetching user: id={user_id}")

    user = USER_DB.get(user_id)
    if not user:
        log.warning(f"User not found: id={user_id}")
        return format_error(f"User {user_id} not found", error_code="NOT_FOUND")

    return format_response(user)


def list_users():
    """Simulate GET /api/users"""
    log.info(f"Listing all users. Total: {len(USER_DB)}")
    users = list(USER_DB.values())
    return format_response(users, message=f"{len(users)} users found")


def delete_user(user_id):
    """Simulate DELETE /api/users/{id}"""
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
    """Pretty print a response dict."""
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
    print(f"\nLog file written to: mini_projects/api_simulator/api.log")