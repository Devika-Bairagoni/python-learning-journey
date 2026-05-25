"""
backend_utils.config

Application configuration class.
Loads config from a dict (or JSON file) and exposes
typed properties with validation.
"""

from backend_utils.validators import validate_port, validate_environment


class AppConfig:
    """
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
    """

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