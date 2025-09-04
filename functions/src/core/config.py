"""Configuration constants and settings for the horoscope application."""

# CORS headers for all responses
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
}

# Zodiac signs in Italian (keeping original names as they're astrological terms)
ZODIAC_SIGNS = [
    "Ariete", "Toro", "Gemelli", "Cancro", "Leone", "Vergine",
    "Bilancia", "Scorpione", "Sagittario", "Capricorno", "Acquario", "Pesci"
]

# Aspect constants
ASPECTS = {
    "Conjunction": 0,
    "Sextile": 60,
    "Square": 90,
    "Trine": 120,
    "Opposition": 180,
}

# Default orb tolerance for aspect calculations
DEFAULT_ORB = 6.0

# Firebase region
FIREBASE_REGION = "europe-west1"
