"""Main entry point for Firebase Functions.

This file imports all function endpoints to make them available for deployment.
"""

from firebase_admin import initialize_app

# Import all function endpoints to register them
from src.api.horoscope import calculate_horoscope
from src.api.aspects import calculate_aspects
from src.api.moon_phase import moon_phase

# Initialize Firebase Admin SDK
initialize_app()

# All functions are now available for deployment:
# - calculate_horoscope
# - calculate_aspects  
# - moon_phase
