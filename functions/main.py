"""Main entry point for Firebase Functions.

This file imports all function endpoints to make them available for deployment.
"""

import sys
import os
from firebase_admin import initialize_app

# Add the current directory to Python path so we can import src modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
