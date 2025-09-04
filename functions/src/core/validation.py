"""Request validation and data parsing functions."""

import json
import os
from typing import Tuple, Optional
from firebase_functions import https_fn
from .config import CORS_HEADERS


def handle_cors_preflight(req: https_fn.Request) -> Optional[https_fn.Response]:
    """Handle CORS preflight OPTIONS request."""
    if req.method == 'OPTIONS':
        return https_fn.Response('', status=204, headers=CORS_HEADERS)
    return None


def validate_request_method(req: https_fn.Request) -> Optional[https_fn.Response]:
    """Validate that request is POST method."""
    if req.method != 'POST':
        return https_fn.Response(
            json.dumps({'error': 'Method not allowed'}),
            status=405,
            headers=CORS_HEADERS
        )
    return None


def parse_and_validate_birth_data(req: https_fn.Request) -> Tuple[Optional[Tuple[int, int, int]], Optional[Tuple[int, int, int]], Optional[float], Optional[float], Optional[float], Optional[https_fn.Response]]:
    """
    Parse and validate birth data from request.
    Returns: (date, time, latitude, longitude, timezone_offset, error_response)
    """
    data = req.get_json()
    
    if not data:
        return None, None, None, None, None, https_fn.Response(
            json.dumps({'error': 'No JSON data provided'}),
            status=400,
            headers=CORS_HEADERS
        )
    
    # Validate required fields
    required_fields = ['date', 'time', 'latitude', 'longitude']
    for field in required_fields:
        if field not in data:
            return None, None, None, None, None, https_fn.Response(
                json.dumps({'error': f'Missing required field: {field}'}),
                status=400,
                headers=CORS_HEADERS
            )
    
    try:
        # Extract and validate data
        date = tuple(data['date'])
        time = tuple(data['time'])
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        timezone_offset = float(data.get('timezone_offset_hours', 0.0))
        
        # Validate date and time format
        if len(date) != 3 or len(time) != 3:
            return None, None, None, None, None, https_fn.Response(
                json.dumps({'error': 'Date and time must be arrays of 3 elements [year, month, day] and [hour, minute, second]'}),
                status=400,
                headers=CORS_HEADERS
            )
        
        return date, time, latitude, longitude, timezone_offset, None
        
    except ValueError as e:
        return None, None, None, None, None, https_fn.Response(
            json.dumps({'error': f'Invalid data format: {str(e)}'}),
            status=400,
            headers=CORS_HEADERS
        )


def validate_authorization(req: https_fn.Request) -> Optional[https_fn.Response]:
    """Validate Authorization header against API_KEY environment variable."""
    api_key = os.getenv('API_KEY')
    
    if not api_key:
        return https_fn.Response(
            json.dumps({'error': 'API key not configured'}),
            status=500,
            headers=CORS_HEADERS
        )
    
    auth_header = req.headers.get('Authorization')
    if not auth_header:
        return https_fn.Response(
            json.dumps({'error': 'Authorization header required'}),
            status=401,
            headers=CORS_HEADERS
        )
    
    # Support both "Bearer <token>" and direct token formats
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
    else:
        token = auth_header
    
    if token != api_key:
        return https_fn.Response(
            json.dumps({'error': 'Invalid API key'}),
            status=401,
            headers=CORS_HEADERS
        )
    
    return None
