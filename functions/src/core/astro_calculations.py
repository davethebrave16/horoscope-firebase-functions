"""Astrological calculation functions using Swiss Ephemeris."""

import swisseph as swe
from typing import Dict, Tuple, List
from .config import ZODIAC_SIGNS, ASPECTS, DEFAULT_ORB

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


def calculate_planetary_aspects(positions: Dict[str, Tuple[str, int, float, float]], orb: float = DEFAULT_ORB) -> List[Dict[str, str]]:
    """
    Calculate aspects between planets and houses.
    
    Args:
        positions: Dictionary with planetary and house positions
        orb: Orb tolerance in degrees (default from config)
        
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
