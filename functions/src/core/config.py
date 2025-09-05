"""Configuration constants and settings for the horoscope application."""

# CORS headers for all responses
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
}

# Zodiac signs in English
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
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

# Lenormand card mapping based on Moon's sign and decan
LENORMAND_CARDS = {
    # Sign: {decan: card_name}
    "Aries": {1: "Rider", 2: "Clover", 3: "Ship"},
    "Taurus": {1: "House", 2: "Tree", 3: "Clouds"},
    "Gemini": {1: "Snake", 2: "Coffin", 3: "Bouquet"},
    "Cancer": {1: "Scythe", 2: "Whip", 3: "Birds"},
    "Leo": {1: "Child", 2: "Fox", 3: "Bear"},
    "Virgo": {1: "Stars", 2: "Stork", 3: "Dog"},
    "Libra": {1: "Tower", 2: "Garden", 3: "Mountain"},
    "Scorpio": {1: "Paths", 2: "Mice", 3: "Heart"},
    "Sagittarius": {1: "Ring", 2: "Book", 3: "Letter"},
    "Capricorn": {1: "Man", 2: "Woman", 3: "Lily"},
    "Aquarius": {1: "Sun", 2: "Moon", 3: "Key"},
    "Pisces": {1: "Fish", 2: "Anchor", 3: "Cross"}
}

