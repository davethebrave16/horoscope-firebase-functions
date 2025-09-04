"""Moon phase calculation API endpoint."""

from firebase_functions import https_fn
from ..core.astro_calculations import calculate_positions, moon_ascending_descending
from ..core.validation import (
    handle_cors_preflight,
    validate_authorization,
    validate_request_method,
    parse_and_validate_birth_data
)
from ..utils.response_utils import create_success_response, create_error_response
from ..core.config import FIREBASE_REGION


@https_fn.on_request(region=FIREBASE_REGION)
def moon_phase(req: https_fn.Request) -> https_fn.Response:
    """
    Firebase HTTP function to determine if the Moon is ascending or descending.
    
    Expected JSON payload:
    {
        "date": [year, month, day],
        "time": [hour, minute, second],
        "latitude": float,
        "longitude": float,
        "timezone_offset_hours": float (optional, defaults to 0)
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
        
        # Calculate positions first
        positions = calculate_positions(
            date=date,
            time=time,
            latitude=latitude,
            longitude=longitude,
            timezone_offset_hours=timezone_offset
        )
        
        # Determine Moon phase
        moon_phase_result = moon_ascending_descending(positions)
        
        # Get Moon position details
        moon_sign, moon_decan, moon_degree_in_sign, moon_absolute_longitude = positions["Moon"]
        ascendant_longitude = positions["Ascendant"][3]
        descendant_longitude = positions["Descendant"][3]
        
        # Format response
        response_data = {
            'success': True,
            'moon_phase': moon_phase_result,
            'moon_position': {
                'sign': moon_sign,
                'decan': moon_decan,
                'degree_in_sign': round(moon_degree_in_sign, 2),
                'absolute_longitude': round(moon_absolute_longitude, 2)
            },
            'reference_points': {
                'ascendant_longitude': round(ascendant_longitude, 2),
                'descendant_longitude': round(descendant_longitude, 2)
            },
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
