"""
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
"""

from datetime import datetime


def format_response(data, message=None):
    """
    Format a successful API response.

    Args:
        data: The response payload (dict, list, or scalar)
        message: Optional human-readable message

    Returns:
        dict: Standardised success response
    """
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
    """
    Format a failed API response.

    Args:
        error_message: Human-readable error description
        error_code: Optional machine-readable error code

    Returns:
        dict: Standardised error response
    """
    response = {
        "success":   False,
        "data":      None,
        "error":     error_message,
        "timestamp": datetime.utcnow().isoformat(),
    }
    if error_code:
        response["error_code"] = error_code
    return response