"""
config_loader.py

Production-grade configuration loader with full exception handling.
Loads app config from JSON, validates required fields and types,
and provides safe access to all config values.

Real-world relevance:
  - Every backend service has a config loader exactly like this
  - FastAPI, Django, Flask all use similar config validation
  - This pattern appears in AWS Lambda, Docker containers, cloud functions

Usage:
    python mini_projects/config_loader/config_loader.py

Author: [Your Name]
Date: [Today's Date]
"""

import json


# --- Custom exceptions for this module ---

class ConfigLoadError(Exception):
    """Raised when config file cannot be loaded or parsed."""
    pass


class ConfigValidationError(Exception):
    """Raised when config is missing required fields or has invalid values."""

    def __init__(self, field: str, reason: str):
        self.field = field
        self.reason = reason
        super().__init__(f"Config validation failed — '{field}': {reason}")


# --- Config schema: what we require and what types we expect ---

REQUIRED_FIELDS = {
    "app_name": str,
    "environment": str,
    "server": dict,
}

VALID_ENVIRONMENTS = ["development", "staging", "production"]


def load_config_file(filepath: str) -> dict:
    """
    Load and parse a JSON config file.
    Raises ConfigLoadError for file or parsing issues.
    """
    try:
        with open(filepath, "r") as f:
            return json.load(f)

    except FileNotFoundError:
        raise ConfigLoadError(
            f"Config file not found: '{filepath}'\n"
            f"  Tip: Check that the file path is correct."
        )

    except json.JSONDecodeError as e:
        raise ConfigLoadError(
            f"Config file contains invalid JSON: '{filepath}'\n"
            f"  JSON error: {e.msg} at line {e.lineno}, column {e.colno}"
        )

    except PermissionError:
        raise ConfigLoadError(
            f"Permission denied reading config: '{filepath}'"
        )


def validate_config(config: dict) -> None:
    """
    Validate config against required schema.
    Raises ConfigValidationError for any violation.
    """
    # Check required fields exist with correct types
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in config:
            raise ConfigValidationError(field, "required field is missing")

        if not isinstance(config[field], expected_type):
            actual = type(config[field]).__name__
            expected = expected_type.__name__
            raise ConfigValidationError(
                field,
                f"expected {expected}, got {actual}"
            )

    # Validate environment value
    env = config["environment"]
    if env not in VALID_ENVIRONMENTS:
        raise ConfigValidationError(
            "environment",
            f"must be one of {VALID_ENVIRONMENTS}, got '{env}'"
        )

    # Validate server.port if present
    server = config.get("server", {})
    if "port" in server:
        port = server["port"]
        if not isinstance(port, int):
            raise ConfigValidationError(
                "server.port",
                f"must be an integer, got {type(port).__name__} ('{port}')"
            )
        if not (1 <= port <= 65535):
            raise ConfigValidationError(
                "server.port",
                f"must be between 1 and 65535, got {port}"
            )


def get_config_value(config: dict, *keys, default=None):
    """
    Safely retrieve a nested config value using a key path.

    Example:
        get_config_value(config, "server", "port", default=8000)
        → config["server"]["port"] safely
    """
    current = config
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
        if current is default:
            return default
    return current


def load_and_validate(filepath: str) -> dict:
    """
    Full pipeline: load file → parse JSON → validate schema.
    Returns validated config dict or raises descriptive errors.
    """
    config = load_config_file(filepath)    # may raise ConfigLoadError
    validate_config(config)                # may raise ConfigValidationError
    return config


def print_config_summary(config: dict) -> None:
    """Print a safe summary of loaded config (never print passwords)."""
    print("=" * 50)
    print("  CONFIG LOADED SUCCESSFULLY")
    print("=" * 50)
    print(f"  App         : {config.get('app_name')}")
    print(f"  Version     : {config.get('version', 'not specified')}")
    print(f"  Environment : {config.get('environment')}")
    print(f"  Host        : {get_config_value(config, 'server', 'host')}")
    print(f"  Port        : {get_config_value(config, 'server', 'port')}")
    print(f"  DB Host     : {get_config_value(config, 'database', 'host', default='not configured')}")
    print(f"  Log Level   : {get_config_value(config, 'logging', 'level', default='not configured')}")
    print("=" * 50)


if __name__ == "__main__":
    BASE_PATH = "mini_projects/config_loader"

    # --- Test 1: Valid config ---
    print("TEST 1: Loading valid config")
    print("-" * 35)
    try:
        config = load_and_validate(f"{BASE_PATH}/config_valid.json")
        print_config_summary(config)
    except ConfigLoadError as e:
        print(f"  Load error: {e}")
    except ConfigValidationError as e:
        print(f"  Validation error: {e}")

    print()

    # --- Test 2: Invalid config (bad port type) ---
    print("TEST 2: Loading invalid config")
    print("-" * 35)
    try:
        config = load_and_validate(f"{BASE_PATH}/config_invalid.json")
        print_config_summary(config)
    except ConfigLoadError as e:
        print(f"  Load error: {e}")
    except ConfigValidationError as e:
        print(f"  Validation error: {e}")
        print(f"  Field   : {e.field}")
        print(f"  Reason  : {e.reason}")

    print()

    # --- Test 3: Missing file ---
    print("TEST 3: Loading missing file")
    print("-" * 35)
    try:
        config = load_and_validate(f"{BASE_PATH}/config_missing.json")
        print_config_summary(config)
    except ConfigLoadError as e:
        print(f"  Load error: {e}")
    except ConfigValidationError as e:
        print(f"  Validation error: {e}")