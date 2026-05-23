"""
custom_exceptions.py

Custom exceptions: define your own error types for your application domain.
This is what separates a professional codebase from a beginner codebase.

Why custom exceptions:
  - Clear, meaningful error names instead of generic ValueError
  - Callers can catch YOUR specific errors separately from Python errors
  - Self-documenting — the exception name tells you what went wrong
  - Industry standard in every production Python codebase

Author: [Your Name]
"""


# --- Defining custom exceptions ---
# Always inherit from Exception (or a more specific base class).
# Keep them simple — usually just a class name and docstring is enough.

class ConfigurationError(Exception):
    """Raised when application configuration is invalid or missing."""
    pass


class ServerNotFoundError(Exception):
    """Raised when a requested server ID does not exist in inventory."""
    pass


class HealthCheckFailedError(Exception):
    """Raised when a server fails its health check."""

    def __init__(self, server_name: str, reason: str):
        # Custom __init__ lets you attach structured data to the exception
        self.server_name = server_name
        self.reason = reason
        # Call parent __init__ with a formatted message
        super().__init__(f"Health check failed for '{server_name}': {reason}")


# --- Using custom exceptions ---

def load_server_config(config: dict) -> dict:
    """
    Validate and load server config dict.
    Raises ConfigurationError if required fields are missing.
    """
    required_fields = ["host", "port", "environment"]

    for field in required_fields:
        if field not in config:
            # Raise YOUR exception with a clear message
            raise ConfigurationError(
                f"Missing required config field: '{field}'"
            )

    if not isinstance(config["port"], int):
        raise ConfigurationError(
            f"'port' must be an integer, got {type(config['port']).__name__}"
        )

    return config


def get_server_by_id(inventory: list, server_id: str) -> dict:
    """
    Find a server by ID.
    Raises ServerNotFoundError if not found.
    """
    for server in inventory:
        if server["id"] == server_id:
            return server

    raise ServerNotFoundError(
        f"No server with ID '{server_id}' found in inventory"
    )


def perform_health_check(server: dict) -> None:
    """
    Simulate a health check. Raises HealthCheckFailedError if unhealthy.
    """
    if server["status"] == "stopped":
        raise HealthCheckFailedError(server["name"], "Server is stopped")

    if server.get("cpu_usage", 0) > 90:
        raise HealthCheckFailedError(
            server["name"],
            f"CPU usage critical: {server['cpu_usage']}%"
        )


# --- Catching custom exceptions ---
print("=== Custom Exception Handling ===")

# Test 1: Missing config field
try:
    config = {"host": "localhost", "port": 8000}  # missing 'environment'
    load_server_config(config)
except ConfigurationError as e:
    print(f"  Config error: {e}")

# Test 2: Valid config
try:
    config = {"host": "localhost", "port": 8000, "environment": "dev"}
    validated = load_server_config(config)
    print(f"  Config loaded: {validated}")
except ConfigurationError as e:
    print(f"  Config error: {e}")

# Test 3: Server not found
inventory = [
    {"id": "srv-001", "name": "api-01", "status": "running", "cpu_usage": 45},
    {"id": "srv-002", "name": "db-01",  "status": "stopped", "cpu_usage": 0},
]

try:
    server = get_server_by_id(inventory, "srv-999")
except ServerNotFoundError as e:
    print(f"  Not found: {e}")

# Test 4: Health check failure
try:
    server = get_server_by_id(inventory, "srv-002")
    perform_health_check(server)
    print(f"  {server['name']} is healthy")
except ServerNotFoundError as e:
    print(f"  Not found: {e}")
except HealthCheckFailedError as e:
    # Access the structured data attached to the exception
    print(f"  Alert: {e}")
    print(f"  Server: {e.server_name}, Reason: {e.reason}")