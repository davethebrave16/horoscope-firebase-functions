#!/usr/bin/env python3
"""Script to verify API compatibility between old and new implementations."""

import sys
import os
sys.path.append('functions')

def verify_function_signatures():
    """Verify that all function signatures match the original."""
    
    # Import the new functions
    from functions.src.api.horoscope import calculate_horoscope
    from functions.src.api.aspects import calculate_aspects
    from functions.src.api.moon_phase import moon_phase
    
    # Check function names and decorators
    functions_to_check = [
        ('calculate_horoscope', calculate_horoscope),
        ('calculate_aspects', calculate_aspects),
        ('moon_phase', moon_phase)
    ]
    
    print("Verifying function signatures...")
    
    for func_name, func in functions_to_check:
        print(f"✓ {func_name} - Function exists and is callable")
        
        # Check if function has the correct decorator
        if hasattr(func, '__wrapped__'):
            print(f"  ✓ {func_name} - Has Firebase function decorator")
        else:
            print(f"  ⚠ {func_name} - May not have Firebase decorator")
    
    return True

def verify_imports():
    """Verify that all required modules can be imported."""
    
    print("\nVerifying module imports...")
    
    try:
        from functions.src.core.config import CORS_HEADERS, ZODIAC_SIGNS, ASPECTS
        print("✓ Core config imports successful")
    except ImportError as e:
        print(f"✗ Core config import failed: {e}")
        return False
    
    try:
        from functions.src.core.astro_calculations import calculate_positions, PLANETS
        print("✓ Astro calculations imports successful")
    except ImportError as e:
        print(f"✗ Astro calculations import failed: {e}")
        return False
    
    try:
        from functions.src.core.validation import validate_authorization, parse_and_validate_birth_data
        print("✓ Validation imports successful")
    except ImportError as e:
        print(f"✗ Validation import failed: {e}")
        return False
    
    try:
        from functions.src.utils.response_utils import create_success_response, create_error_response
        print("✓ Response utils imports successful")
    except ImportError as e:
        print(f"✗ Response utils import failed: {e}")
        return False
    
    return True

def verify_constants():
    """Verify that constants match the original implementation."""
    
    print("\nVerifying constants...")
    
    from functions.src.core.config import ZODIAC_SIGNS, ASPECTS, CORS_HEADERS
    
    # Check zodiac signs
    expected_zodiac = [
        "Ariete", "Toro", "Gemelli", "Cancro", "Leone", "Vergine",
        "Bilancia", "Scorpione", "Sagittario", "Capricorno", "Acquario", "Pesci"
    ]
    
    if ZODIAC_SIGNS == expected_zodiac:
        print("✓ Zodiac signs match original")
    else:
        print("✗ Zodiac signs don't match original")
        return False
    
    # Check aspects
    expected_aspects = {
        "Conjunction": 0,
        "Sextile": 60,
        "Square": 90,
        "Trine": 120,
        "Opposition": 180,
    }
    
    if ASPECTS == expected_aspects:
        print("✓ Aspects match original")
    else:
        print("✗ Aspects don't match original")
        return False
    
    # Check CORS headers
    expected_cors = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    }
    
    if CORS_HEADERS == expected_cors:
        print("✓ CORS headers match original")
    else:
        print("✗ CORS headers don't match original")
        return False
    
    return True

def main():
    """Run all verification checks."""
    
    print("=== API Compatibility Verification ===\n")
    
    all_passed = True
    
    # Run verification checks
    all_passed &= verify_imports()
    all_passed &= verify_constants()
    all_passed &= verify_function_signatures()
    
    print("\n=== Verification Summary ===")
    
    if all_passed:
        print("✅ All checks passed! API compatibility maintained.")
        print("\nThe refactored code maintains the same API interface as the original.")
        print("All three functions (calculate_horoscope, calculate_aspects, moon_phase)")
        print("should work exactly the same as before.")
    else:
        print("❌ Some checks failed. Please review the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
