"""
backend_utils.logger

Structured logger for backend applications.
Wraps Python logging with consistent formatting and log levels.
"""

import logging
from datetime import datetime
from pathlib import Path


class Logger:
    """
    Structured application logger.
    Creates consistent log format across all modules.

    Usage:
        log = Logger("api_service")
        log.info("Server started on port 8000")
        log.error("Database connection failed")
    """

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