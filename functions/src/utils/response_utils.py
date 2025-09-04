"""Response utility functions for consistent API responses."""

import json
from firebase_functions import https_fn
from ..core.config import CORS_HEADERS


def create_error_response(error_message: str, status: int = 500) -> https_fn.Response:
    """Create standardized error response."""
    return https_fn.Response(
        json.dumps({'error': error_message}),
        status=status,
        headers=CORS_HEADERS
    )


def create_success_response(data: dict) -> https_fn.Response:
    """Create standardized success response."""
    return https_fn.Response(
        json.dumps(data, indent=2),
        status=200,
        headers=CORS_HEADERS
    )
