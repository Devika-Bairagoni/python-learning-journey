"""
backend_utils
A reusable internal utilities package for backend engineering.

Exposes the most commonly used utilities at the package level
so callers can import directly from backend_utils instead of
navigating deep module paths.

Usage:
    from backend_utils import Logger, format_response, validate_port
"""

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