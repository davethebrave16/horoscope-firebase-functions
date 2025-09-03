import swisseph as swe
from typing import Dict, Tuple
from firebase_functions import https_fn
from firebase_admin import initialize_app
import json

# Initialize Firebase Admin
initialize_app()

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

@https_fn.on_request()
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
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    
    # Handle preflight OPTIONS request
    if req.method == 'OPTIONS':
        return https_fn.Response('', status=204, headers=headers)
    
    # Only allow POST requests
    if req.method != 'POST':
        return https_fn.Response(
            json.dumps({'error': 'Method not allowed'}),
            status=405,
            headers=headers
        )
    
    try:
        # Parse request data
        data = req.get_json()
        
        if not data:
            return https_fn.Response(
                json.dumps({'error': 'No JSON data provided'}),
                status=400,
                headers=headers
            )
        
        # Validate required fields
        required_fields = ['date', 'time', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return https_fn.Response(
                    json.dumps({'error': f'Missing required field: {field}'}),
                    status=400,
                    headers=headers
                )
        
        # Extract and validate data
        date = tuple(data['date'])
        time = tuple(data['time'])
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        timezone_offset = float(data.get('timezone_offset_hours', 0.0))
        
        # Validate date and time format
        if len(date) != 3 or len(time) != 3:
            return https_fn.Response(
                json.dumps({'error': 'Date and time must be arrays of 3 elements [year, month, day] and [hour, minute, second]'}),
                status=400,
                headers=headers
            )
        
        # Calculate positions
        positions = calculate_positions(
            date=date,
            time=time,
            latitude=latitude,
            longitude=longitude,
            timezone_offset_hours=timezone_offset
        )
        
        # Format response
        response_data = {
            'success': True,
            'positions': positions,
            'input_data': {
                'date': date,
                'time': time,
                'latitude': latitude,
                'longitude': longitude,
                'timezone_offset_hours': timezone_offset
            }
        }
        
        return https_fn.Response(
            json.dumps(response_data, indent=2),
            status=200,
            headers=headers
        )
        
    except ValueError as e:
        return https_fn.Response(
            json.dumps({'error': f'Invalid data format: {str(e)}'}),
            status=400,
            headers=headers
        )
    except Exception as e:
        return https_fn.Response(
            json.dumps({'error': f'Internal server error: {str(e)}'}),
            status=500,
            headers=headers
        )
