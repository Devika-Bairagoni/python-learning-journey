"""
backend_utils.validators

Input validation functions used across backend services.
All validators return the validated value or raise ValueError.
"""

import re

VALID_ENVIRONMENTS = ["development", "staging", "production"]


def validate_port(port):
    """
    Validate a network port number.
    Returns port as int if valid, raises ValueError if not.
    """
    try:
        port = int(port)
    except (TypeError, ValueError):
        raise ValueError(f"Port must be a number, got: {port!r}")

    if not (1 <= port <= 65535):
        raise ValueError(f"Port must be between 1 and 65535, got: {port}")

    return port


def validate_email(email):
    """
    Validate email address format using regex.
    Returns email if valid, raises ValueError if not.
    """
    if not isinstance(email, str):
        raise ValueError(f"Email must be a string, got {type(email).__name__}")

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise ValueError(f"Invalid email format: {email!r}")

    return email.lower().strip()


def validate_environment(environment):
    """
    Validate deployment environment string.
    Returns environment if valid, raises ValueError if not.
    """
    if environment not in VALID_ENVIRONMENTS:
        raise ValueError(
            f"Environment must be one of {VALID_ENVIRONMENTS}, "
            f"got: {environment!r}"
        )
    return environment