"""Planetary transits over cardinal points API endpoint."""

from firebase_functions import https_fn
from ..core.astro_calculations import calculate_planetary_transits, PLANETS
from ..core.validation import (
    handle_cors_preflight,
    validate_authorization,
    validate_request_method,
)
from ..utils.response_utils import create_success_response, create_error_response
from ..core.config import FIREBASE_REGION


@https_fn.on_request(region=FIREBASE_REGION)
def planetary_transits(req: https_fn.Request) -> https_fn.Response:
    """
    Firebase HTTP function to calculate planetary transits over cardinal points.
    
    Expected JSON payload:
    {
        "year": int,
        "month": int,
        "latitude": float,
        "longitude": float,
        "timezone_offset_hours": float (optional, defaults to 0),
        "planet": str (optional, defaults to "Moon"),
        "step_minutes": int (optional, defaults to 15)
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
        # Parse request data
        if not req.is_json:
            return create_error_response("Request must be JSON")
        
        data = req.get_json()
        
        # Validate required fields
        required_fields = ["year", "month", "latitude", "longitude"]
        for field in required_fields:
            if field not in data:
                return create_error_response(f"Missing required field: {field}")
        
        # Extract and validate data
        year = data["year"]
        month = data["month"]
        latitude = data["latitude"]
        longitude = data["longitude"]
        timezone_offset = data.get("timezone_offset_hours", 0.0)
        planet = data.get("planet", "Moon")
        step_minutes = data.get("step_minutes", 15)
        
        # Validate data types and ranges
        if not isinstance(year, int) or year < 1900 or year > 2100:
            return create_error_response("Year must be an integer between 1900 and 2100")
        
        if not isinstance(month, int) or month < 1 or month > 12:
            return create_error_response("Month must be an integer between 1 and 12")
        
        if not isinstance(latitude, (int, float)) or latitude < -90 or latitude > 90:
            return create_error_response("Latitude must be a number between -90 and 90")
        
        if not isinstance(longitude, (int, float)) or longitude < -180 or longitude > 180:
            return create_error_response("Longitude must be a number between -180 and 180")
        
        if not isinstance(timezone_offset, (int, float)) or timezone_offset < -12 or timezone_offset > 14:
            return create_error_response("Timezone offset must be a number between -12 and 14")
        
        if planet not in PLANETS:
            return create_error_response(f"Planet must be one of: {', '.join(PLANETS.keys())}")
        
        if not isinstance(step_minutes, int) or step_minutes < 1 or step_minutes > 60:
            return create_error_response("Step minutes must be an integer between 1 and 60")
        
        # Calculate transits
        transits = calculate_planetary_transits(
            year=year,
            month=month,
            lat=latitude,
            lon=longitude,
            tz_offset_hours=timezone_offset,
            planet_name=planet,
            step_minutes=step_minutes
        )
        
        # Format response
        formatted_transits = []
        for transit in transits:
            formatted_transits.append({
                "planet": transit.planet,
                "angle": transit.angle,
                "datetime_local": transit.datetime_local.isoformat(),
                "longitude": round(transit.longitude, 6),
                "sign": transit.sign,
                "degree_in_sign": round(transit.degree_in_sign, 2),
                "decan": transit.decan
            })
        
        response_data = {
            "success": True,
            "transits": formatted_transits,
            "parameters": {
                "year": year,
                "month": month,
                "location": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "timezone_offset_hours": timezone_offset
                },
                "planet": planet,
                "step_minutes": step_minutes
            },
            "total_transits": len(formatted_transits)
        }
        
        return create_success_response(response_data)
        
    except ValueError as e:
        return create_error_response(f"Invalid input: {str(e)}")
    except Exception as e:
        return create_error_response(f"Internal server error: {str(e)}")
