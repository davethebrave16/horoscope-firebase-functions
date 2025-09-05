"""Moon phase calculation API endpoint."""

from firebase_functions import https_fn
from ..core.astro_calculations import calculate_moon_phase
from ..core.validation import (
    handle_cors_preflight,
    validate_authorization,
    validate_request_method
)
from ..utils.response_utils import create_success_response, create_error_response
from ..core.config import FIREBASE_REGION


@https_fn.on_request(region=FIREBASE_REGION)
def moon_phase(req: https_fn.Request) -> https_fn.Response:
    """
    Firebase HTTP function to calculate the moon phase for a given date and time.
    
    Expected JSON payload:
    {
        "date": [year, month, day],
        "time": [hour, minute, second] (optional, defaults to [0, 0, 0])
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
        # Parse JSON request
        if not req.is_json:
            return create_error_response('Request must be JSON', 400)
        
        data = req.get_json()
        if not data:
            return create_error_response('Invalid JSON data', 400)
        
        # Validate required fields
        if 'date' not in data:
            return create_error_response('Missing required field: date', 400)
        
        date = data['date']
        if not isinstance(date, list) or len(date) != 3:
            return create_error_response('Date must be an array [year, month, day]', 400)
        
        year, month, day = date
        if not all(isinstance(x, int) for x in [year, month, day]):
            return create_error_response('Date values must be integers', 400)
        
        if not (1 <= month <= 12):
            return create_error_response('Month must be between 1 and 12', 400)
        
        if not (1 <= day <= 31):
            return create_error_response('Day must be between 1 and 31', 400)
        
        # Validate time (optional)
        time = data.get('time', [0, 0, 0])
        if not isinstance(time, list) or len(time) != 3:
            return create_error_response('Time must be an array [hour, minute, second]', 400)
        
        hour, minute, second = time
        if not all(isinstance(x, int) for x in [hour, minute, second]):
            return create_error_response('Time values must be integers', 400)
        
        if not (0 <= hour <= 23):
            return create_error_response('Hour must be between 0 and 23', 400)
        
        if not (0 <= minute <= 59):
            return create_error_response('Minute must be between 0 and 59', 400)
        
        if not (0 <= second <= 59):
            return create_error_response('Second must be between 0 and 59', 400)
        
        # Calculate moon phase
        moon_phase_data = calculate_moon_phase(year, month, day, hour, minute, second)
        
        # Format response
        response_data = {
            'success': True,
            'moon_phase': {
                'phase_name': moon_phase_data['phase_name'],
                'age_days': moon_phase_data['age_days'],
                'fraction_of_cycle': moon_phase_data['fraction_of_cycle'],
                'illuminated_fraction': moon_phase_data['illuminated_fraction'],
                'julian_date': moon_phase_data['julian_date']
            },
            'request_data': {
                'date': {
                    'year': year,
                    'month': month,
                    'day': day
                },
                'time': {
                    'hour': hour,
                    'minute': minute,
                    'second': second
                }
            }
        }
        
        return create_success_response(response_data)
        
    except Exception as e:
        return create_error_response(f'Internal server error: {str(e)}')
