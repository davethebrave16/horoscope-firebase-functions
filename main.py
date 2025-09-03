import swisseph as swe
from typing import Dict, Tuple, List
from firebase_functions import https_fn
from firebase_admin import initialize_app
import json
import os

# Initialize Firebase Admin
initialize_app()

# Common CORS headers
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
}

def handle_cors_preflight(req: https_fn.Request) -> https_fn.Response:
    """Handle CORS preflight OPTIONS request."""
    if req.method == 'OPTIONS':
        return https_fn.Response('', status=204, headers=CORS_HEADERS)
    return None

def validate_request_method(req: https_fn.Request) -> https_fn.Response:
    """Validate that request is POST method."""
    if req.method != 'POST':
        return https_fn.Response(
            json.dumps({'error': 'Method not allowed'}),
            status=405,
            headers=CORS_HEADERS
        )
    return None

def parse_and_validate_birth_data(req: https_fn.Request) -> tuple:
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

def validate_authorization(req: https_fn.Request) -> https_fn.Response:
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

# Zodiac signs in Italian (keeping original names as they're astrological terms)
ZODIAC_SIGNS = [
    "Ariete", "Toro", "Gemelli", "Cancro", "Leone", "Vergine",
    "Bilancia", "Scorpione", "Sagittario", "Capricorno", "Acquario", "Pesci"
]

# Planet constants from Swiss Ephemeris
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
}

def get_sign_and_decan(longitude: float) -> Tuple[str, int, float]:
    """
    Calculate zodiac sign, decan, and degree within sign from longitude.
    
    Args:
        longitude: Ecliptic longitude in degrees
        
    Returns:
        Tuple of (sign_name, decan_number, degree_in_sign)
    """
    longitude = longitude % 360.0
    sign_index = int(longitude // 30)
    sign = ZODIAC_SIGNS[sign_index]
    degree_in_sign = longitude - sign_index * 30.0

    if degree_in_sign < 10:
        decan = 1
    elif degree_in_sign < 20:
        decan = 2
    else:
        decan = 3

    return sign, decan, degree_in_sign

def calculate_positions(
    date: Tuple[int, int, int],
    time: Tuple[int, int, int],
    latitude: float,
    longitude: float,
    timezone_offset_hours: float = 0.0,
) -> Dict[str, Tuple[str, int, float, float]]:
    """
    Calculate planetary and house positions for a given birth data.
    
    Args:
        date: Birth date as (year, month, day)
        time: Birth time as (hour, minute, second)
        latitude: Birth latitude in degrees
        longitude: Birth longitude in degrees
        timezone_offset_hours: Timezone offset from UTC in hours
        
    Returns:
        Dictionary with planetary and house positions
    """
    year, month, day = date
    hour, minute, second = time
    local_decimal_time = hour + minute/60.0 + second/3600.0
    ut_time = local_decimal_time - timezone_offset_hours
    jd_ut = swe.julday(year, month, day, ut_time)

    results = {}
    
    # Calculate planetary positions
    for name, code in PLANETS.items():
        ecliptic_longitude = swe.calc_ut(jd_ut, code)[0][0]  # Get the longitude value
        results[name] = (*get_sign_and_decan(ecliptic_longitude), ecliptic_longitude)

    # Calculate house cusps and angles
    cusps, ascmc = swe.houses(jd_ut, latitude, longitude)
    ascendant_longitude = ascmc[0]
    midheaven_longitude = ascmc[1]
    descendant_longitude = (ascendant_longitude + 180.0) % 360.0
    imum_coeli_longitude = (midheaven_longitude + 180.0) % 360.0

    # Add house angles to results
    for name, longitude_value in {
        "Ascendant": ascendant_longitude,
        "Descendant": descendant_longitude,
        "Midheaven": midheaven_longitude,
        "Imum Coeli": imum_coeli_longitude,
    }.items():
        results[name] = (*get_sign_and_decan(longitude_value), longitude_value)

    return results

# Aspect constants
ASPECTS = {
    "Conjunction": 0,
    "Sextile": 60,
    "Square": 90,
    "Trine": 120,
    "Opposition": 180,
}

def calculate_planetary_aspects(positions: Dict[str, Tuple[str, int, float, float]], orb: float = 6) -> List[Dict[str, str]]:
    """
    Calculate aspects between planets and houses.
    
    Args:
        positions: Dictionary with planetary and house positions
        orb: Orb tolerance in degrees (default 6)
        
    Returns:
        List of aspect dictionaries with planet names, aspect type, and degrees
    """
    aspects_found = []
    names = list(positions.keys())

    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            name1, name2 = names[i], names[j]
            lon1 = positions[name1][3]  # Absolute longitude
            lon2 = positions[name2][3]  # Absolute longitude

            diff = abs(lon1 - lon2)
            if diff > 180:
                diff = 360 - diff

            for aspect_name, aspect_degrees in ASPECTS.items():
                if abs(diff - aspect_degrees) <= orb:
                    aspects_found.append({
                        "planet1": name1,
                        "planet2": name2,
                        "aspect": aspect_name,
                        "degrees": round(diff, 2),
                        "orb": round(abs(diff - aspect_degrees), 2)
                    })
    
    return aspects_found

def moon_ascending_descending(positions: Dict[str, Tuple[str, int, float, float]]) -> str:
    """
    Determine if the Moon is ascending or descending:
    - Ascending -> Moon is in the eastern half (from house 1 to 6)
    - Descending -> Moon is in the western half (from house 7 to 12)
    Simplified: compare Moon longitude with Ascendant/Descendant.
    """
    moon_longitude = positions["Moon"][3]
    ascendant_longitude = positions["Ascendant"][3]
    descendant_longitude = positions["Descendant"][3]

    # Normalize differences
    diff_moon_asc = (moon_longitude - ascendant_longitude + 360) % 360
    diff_dsc_asc = (descendant_longitude - ascendant_longitude + 360) % 360

    if diff_moon_asc < diff_dsc_asc:
        return "The Moon is in ascending phase (from Asc to Dsc)."
    else:
        return "The Moon is in descending phase (from Dsc to Asc)."

@https_fn.on_request(region="europe-west1")
def calculate_horoscope(req: https_fn.Request) -> https_fn.Response:
    """
    Firebase HTTP function to calculate horoscope positions.
    
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
        
        # Calculate positions
        positions = calculate_positions(
            date=date,
            time=time,
            latitude=latitude,
            longitude=longitude,
            timezone_offset_hours=timezone_offset
        )
        
        # Format response with readable structure
        formatted_positions = {}
        for name, (sign, decan, degree_in_sign, absolute_longitude) in positions.items():
            formatted_positions[name] = {
                'sign': sign,
                'decan': decan,
                'degree_in_sign': round(degree_in_sign, 2),
                'absolute_longitude': round(absolute_longitude, 2)
            }
        
        response_data = {
            'success': True,
            'horoscope': {
                'planets': {k: v for k, v in formatted_positions.items() if k in PLANETS.keys()},
                'houses': {k: v for k, v in formatted_positions.items() if k not in PLANETS.keys()}
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

@https_fn.on_request(region="europe-west1")
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

@https_fn.on_request(region="europe-west1")
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
