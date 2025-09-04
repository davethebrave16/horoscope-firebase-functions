"""Aspects calculation API endpoint."""

import json
from firebase_functions import https_fn
from ..core.astro_calculations import calculate_positions, calculate_planetary_aspects
from ..core.validation import (
    handle_cors_preflight,
    validate_authorization,
    validate_request_method,
    parse_and_validate_birth_data
)
from ..utils.response_utils import create_success_response, create_error_response
from ..core.config import FIREBASE_REGION


@https_fn.on_request(region=FIREBASE_REGION)
def calculate_aspects(req: https_fn.Request) -> https_fn.Response:
    """
    Firebase HTTP function to calculate aspects between planets and houses.
    
    Expected JSON payload:
    {
        "date": [year, month, day],
        "time": [hour, minute, second],
        "latitude": float,
        "longitude": float,
        "timezone_offset_hours": float (optional, defaults to 0),
        "orb": float (optional, defaults to 6)
    }
    """
    # Handle CORS preflight
    cors_response = handle_cors_preflight(req)
    if cors_response:
        return cors_response
    
    # Validate authorization
    auth_response = validate_authorization(req)
    if auth_response:
        return auth_response
    
    # Validate request method
    method_response = validate_request_method(req)
    if method_response:
        return method_response
    
    try:
        # Parse and validate birth data
        date, time, latitude, longitude, timezone_offset, error_response = parse_and_validate_birth_data(req)
        if error_response:
            return error_response
        
        # Get orb parameter
        data = req.get_json()
        orb = float(data.get('orb', 6.0))
        
        # Calculate positions first
        positions = calculate_positions(
            date=date,
            time=time,
            latitude=latitude,
            longitude=longitude,
            timezone_offset_hours=timezone_offset
        )
        
        # Calculate aspects
        aspects = calculate_planetary_aspects(positions, orb)
        
        # Format response
        response_data = {
            'success': True,
            'aspects': aspects,
            'aspect_count': len(aspects),
            'orb_used': orb,
            'birth_data': {
                'date': {
                    'year': date[0],
                    'month': date[1],
                    'day': date[2]
                },
                'time': {
                    'hour': time[0],
                    'minute': time[1],
                    'second': time[2]
                },
                'location': {
                    'latitude': latitude,
                    'longitude': longitude,
                    'timezone_offset_hours': timezone_offset
                }
            }
        }
        
        return create_success_response(response_data)
        
    except Exception as e:
        return create_error_response(f'Internal server error: {str(e)}')
