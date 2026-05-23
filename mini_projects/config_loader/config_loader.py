import json

class ConfigLoadError(Exception):
    pass

class ConfigValidationError(Exception):
    def __init__(self, field, reason):
        self.field = field
        self.reason = reason
        super().__init__(f"Config validation failed - '{field}': {reason}")

REQUIRED_FIELDS = {"app_name": str, "environment": str, "server": dict}
VALID_ENVIRONMENTS = ["development", "staging", "production"]

def load_config_file(filepath):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ConfigLoadError(f"Config file not found: '{filepath}'")
    except json.JSONDecodeError as e:
        raise ConfigLoadError(f"Config file contains invalid JSON: '{filepath}'")

def validate_config(config):
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in config:
            raise ConfigValidationError(field, "required field is missing")
        if not isinstance(config[field], expected_type):
            actual = type(config[field]).__name__
            expected = expected_type.__name__
            raise ConfigValidationError(field, f"expected {expected}, got {actual}")
    env = config["environment"]
    if env not in VALID_ENVIRONMENTS:
        raise ConfigValidationError("environment", f"must be one of {VALID_ENVIRONMENTS}, got '{env}'")
    server = config.get("server", {})
    if "port" in server:
        port = server["port"]
        if not isinstance(port, int):
            raise ConfigValidationError("server.port", f"must be an integer, got {type(port).__name__}")
        if not (1 <= port <= 65535):
            raise ConfigValidationError("server.port", f"must be between 1 and 65535, got {port}")

def get_config_value(config, *keys, default=None):
    current = config
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
        if current is default:
            return default
    return current

def load_and_validate(filepath):
    config = load_config_file(filepath)
    validate_config(config)
    return config

def print_config_summary(config):
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

    print("TEST 1: Loading valid config")
    print("-" * 35)
    try:
        config = load_and_validate(f"{BASE_PATH}/config_valid.json")
        print_config_summary(config)
    except ConfigLoadError as e:
        print(f"  Load error: {e}")
    except ConfigValidationError as e:
        print(f"  Validation error: {e}")
        print(f"  Field  : {e.field}")
        print(f"  Reason : {e.reason}")

    print()

    print("TEST 2: Loading invalid config")
    print("-" * 35)
    try:
        config = load_and_validate(f"{BASE_PATH}/config_invalid.json")
        print_config_summary(config)
    except ConfigLoadError as e:
        print(f"  Load error: {e}")
    except ConfigValidationError as e:
        print(f"  Validation error: {e}")
        print(f"  Field  : {e.field}")
        print(f"  Reason : {e.reason}")

    print()

    print("TEST 3: Loading missing file")
    print("-" * 35)
    try:
        config = load_and_validate(f"{BASE_PATH}/config_missing.json")
        print_config_summary(config)
    except ConfigLoadError as e:
        print(f"  Load error: {e}")
    except ConfigValidationError as e:
        print(f"  Validation error: {e}")
