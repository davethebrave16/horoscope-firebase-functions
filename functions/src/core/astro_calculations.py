"""Astrological calculation functions using Swiss Ephemeris."""

import swisseph as swe
from typing import Dict, Tuple, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from .config import ZODIAC_SIGNS, ASPECTS, DEFAULT_ORB, LENORMAND_CARDS

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


@dataclass
class Transit:
    """Represents a planetary transit over a cardinal point."""
    planet: str
    angle: str  # Ascendant, Descendant, Midheaven, Imum Coeli
    datetime_local: datetime
    longitude: float  # Ecliptic longitude at transit
    sign: str
    degree_in_sign: float
    decan: int


def wrap360(x: float) -> float:
    """Wrap angle to 0-360 range."""
    return x % 360.0


def signed_delta(a: float, b: float) -> float:
    """Calculate minimum angular difference a-b in (-180, 180]."""
    d = (a - b + 180.0) % 360.0 - 180.0
    return d if d != -180.0 else 180.0


def jd_from_local(dt_local: datetime, tz_offset_hours: float) -> float:
    """Convert local datetime to Julian day."""
    ut_hours = dt_local.hour + dt_local.minute/60 + dt_local.second/3600 - tz_offset_hours
    return swe.julday(dt_local.year, dt_local.month, dt_local.day, ut_hours)


def planet_longitude(jd_ut: float, planet_code: int) -> float:
    """Get planet's ecliptic longitude."""
    return swe.calc_ut(jd_ut, planet_code)[0][0]


def angles_longitude(jd_ut: float, lat: float, lon: float) -> Tuple[float, float, float, float]:
    """Get cardinal points longitudes: (ASC, DSC, MC, IC)."""
    cusps, ascmc = swe.houses(jd_ut, lat, lon)
    asc = ascmc[0]
    mc = ascmc[1]
    dsc = wrap360(asc + 180.0)
    ic = wrap360(mc + 180.0)
    return asc, dsc, mc, ic


def refine_crossing(
    planet_code: int,
    angle_name: str,
    t0: datetime,
    t1: datetime,
    lat: float,
    lon: float,
    tz_offset_hours: float,
    max_iters: int = 30,
) -> Transit:
    """Refine the exact moment when planet longitude equals angle longitude."""
    a = t0
    b = t1
    
    for _ in range(max_iters):
        mid = a + (b - a)/2
        jd_a = jd_from_local(a, tz_offset_hours)
        jd_mid = jd_from_local(mid, tz_offset_hours)

        asc_a, dsc_a, mc_a, ic_a = angles_longitude(jd_a, lat, lon)
        asc_m, dsc_m, mc_m, ic_m = angles_longitude(jd_mid, lat, lon)

        ang_map_a = {"Ascendant": asc_a, "Descendant": dsc_a, "Midheaven": mc_a, "Imum Coeli": ic_a}
        ang_map_m = {"Ascendant": asc_m, "Descendant": dsc_m, "Midheaven": mc_m, "Imum Coeli": ic_m}

        p_a = planet_longitude(jd_a, planet_code)
        p_m = planet_longitude(jd_mid, planet_code)

        fa = signed_delta(p_a, ang_map_a[angle_name])
        fm = signed_delta(p_m, ang_map_m[angle_name])

        if fa == 0:
            b = a
            break
        if fa * fm <= 0:
            b = mid
        else:
            a = mid

        if (b - a).total_seconds() <= 30:  # ~30s precision
            break

    # Final value
    t = a + (b - a)/2
    jd_t = jd_from_local(t, tz_offset_hours)
    asc, dsc, mc, ic = angles_longitude(jd_t, lat, lon)
    ang_map = {"Ascendant": asc, "Descendant": dsc, "Midheaven": mc, "Imum Coeli": ic}
    p_lon = planet_longitude(jd_t, planet_code)
    lon_match = wrap360((p_lon + ang_map[angle_name]) / 2)
    sign, decan, deg = get_sign_and_decan(lon_match)
    return Transit("", angle_name, t, lon_match, sign, deg, decan)


def calculate_planetary_transits(
    year: int,
    month: int,
    lat: float,
    lon: float,
    tz_offset_hours: float,
    planet_name: str,
    step_minutes: int = 15,
) -> List[Transit]:
    """
    Calculate planetary transits over cardinal points for a given month.
    
    Args:
        year: Year
        month: Month (1-12)
        lat: Latitude in degrees
        lon: Longitude in degrees
        tz_offset_hours: Timezone offset from UTC in hours
        planet_name: Name of the planet
        step_minutes: Time step in minutes for scanning
        
    Returns:
        List of Transit objects sorted by datetime
    """
    if planet_name not in PLANETS:
        raise ValueError(f"Planet {planet_name} not supported.")

    start = datetime(year, month, 1, 0, 0, 0)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)

    step = timedelta(minutes=step_minutes)
    pcode = PLANETS[planet_name]

    results: List[Transit] = []
    angles = ["Ascendant", "Descendant", "Midheaven", "Imum Coeli"]

    prev_dt = None
    prev_vals = None
    dt = start
    
    while dt <= end:
        jd = jd_from_local(dt, tz_offset_hours)
        asc, dsc, mc, ic = angles_longitude(jd, lat, lon)
        ang_map = {"Ascendant": asc, "Descendant": dsc, "Midheaven": mc, "Imum Coeli": ic}
        p = planet_longitude(jd, pcode)

        diffs = {aname: signed_delta(p, aval) for aname, aval in ang_map.items()}

        if prev_vals is not None:
            for aname in angles:
                if (diffs[aname] == 0 or 
                    (prev_vals[aname] > 0 and diffs[aname] < 0) or 
                    (prev_vals[aname] < 0 and diffs[aname] > 0)):
                    tr = refine_crossing(pcode, aname, prev_dt, dt, lat, lon, tz_offset_hours)
                    tr.planet = planet_name
                    results.append(tr)
        
        prev_dt = dt
        prev_vals = diffs
        dt += step

    results.sort(key=lambda x: x.datetime_local)
    return results


def calculate_lenormand_card(moon_sign: str, moon_decan: int) -> str:
    """
    Calculate the Lenormand card based on Moon's sign and decan.
    
    Args:
        moon_sign: Moon's zodiac sign
        moon_decan: Moon's decan (1, 2, or 3)
        
    Returns:
        Lenormand card name
    """
    if moon_sign not in LENORMAND_CARDS:
        return "Unknown"
    
    if moon_decan not in LENORMAND_CARDS[moon_sign]:
        return "Unknown"
    
    return LENORMAND_CARDS[moon_sign][moon_decan]
