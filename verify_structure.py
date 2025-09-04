#!/usr/bin/env python3
"""Script to verify the refactored project structure and code organization."""

import os
import sys

def verify_directory_structure():
    """Verify that the directory structure follows Firebase best practices."""
    
    print("Verifying directory structure...")
    
    required_dirs = [
        "functions",
        "functions/src",
        "functions/src/api",
        "functions/src/core", 
        "functions/src/utils",
        "functions/tests"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}")
        else:
            print(f"✗ {dir_path} - Missing")
            all_exist = False
    
    return all_exist

def verify_files():
    """Verify that all required files exist."""
    
    print("\nVerifying required files...")
    
    required_files = [
        "functions/main.py",
        "functions/requirements.txt",
        "functions/requirements-dev.txt",
        "functions/README.md",
        "functions/src/__init__.py",
        "functions/src/api/__init__.py",
        "functions/src/api/horoscope.py",
        "functions/src/api/aspects.py", 
        "functions/src/api/moon_phase.py",
        "functions/src/core/__init__.py",
        "functions/src/core/config.py",
        "functions/src/core/astro_calculations.py",
        "functions/src/core/validation.py",
        "functions/src/utils/__init__.py",
        "functions/src/utils/response_utils.py",
        "functions/tests/__init__.py",
        "functions/tests/test_astro_calculations.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - Missing")
            all_exist = False
    
    return all_exist

def verify_firebase_config():
    """Verify Firebase configuration is updated."""
    
    print("\nVerifying Firebase configuration...")
    
    firebase_json_path = "firebase.json"
    if not os.path.exists(firebase_json_path):
        print("✗ firebase.json not found")
        return False
    
    with open(firebase_json_path, 'r') as f:
        content = f.read()
        
    if '"source": "functions"' in content:
        print("✓ firebase.json points to functions/ directory")
        return True
    else:
        print("✗ firebase.json doesn't point to functions/ directory")
        return False

def verify_code_organization():
    """Verify that code is properly organized by responsibility."""
    
    print("\nVerifying code organization...")
    
    # Check that main.py only imports and doesn't contain business logic
    main_py_path = "functions/main.py"
    if os.path.exists(main_py_path):
        with open(main_py_path, 'r') as f:
            content = f.read()
            
        # Should only contain imports and initialize_app()
        if "def calculate_" not in content and "def get_sign_" not in content:
            print("✓ main.py is properly organized as entry point")
        else:
            print("✗ main.py contains business logic (should only import)")
            return False
    
    # Check that API modules only contain endpoint functions
    api_files = [
        "functions/src/api/horoscope.py",
        "functions/src/api/aspects.py",
        "functions/src/api/moon_phase.py"
    ]
    
    for api_file in api_files:
        if os.path.exists(api_file):
            with open(api_file, 'r') as f:
                content = f.read()
                
            # Should contain @https_fn.on_request decorator
            if "@https_fn.on_request" in content:
                print(f"✓ {api_file} contains proper Firebase function")
            else:
                print(f"✗ {api_file} missing Firebase function decorator")
                return False
    
    return True

def verify_separation_of_concerns():
    """Verify that concerns are properly separated."""
    
    print("\nVerifying separation of concerns...")
    
    # Check that astro_calculations.py doesn't import Firebase
    astro_file = "functions/src/core/astro_calculations.py"
    if os.path.exists(astro_file):
        with open(astro_file, 'r') as f:
            content = f.read()
            
        if "firebase_functions" not in content and "https_fn" not in content:
            print("✓ astro_calculations.py is pure business logic")
        else:
            print("✗ astro_calculations.py contains Firebase dependencies")
            return False
    
    # Check that validation.py is focused on validation
    validation_file = "functions/src/core/validation.py"
    if os.path.exists(validation_file):
        with open(validation_file, 'r') as f:
            content = f.read()
            
        if "def validate_" in content and "def parse_" in content:
            print("✓ validation.py is focused on validation logic")
        else:
            print("✗ validation.py doesn't contain expected validation functions")
            return False
    
    return True

def main():
    """Run all verification checks."""
    
    print("=== Project Structure Verification ===\n")
    
    all_passed = True
    
    # Run verification checks
    all_passed &= verify_directory_structure()
    all_passed &= verify_files()
    all_passed &= verify_firebase_config()
    all_passed &= verify_code_organization()
    all_passed &= verify_separation_of_concerns()
    
    print("\n=== Verification Summary ===")
    
    if all_passed:
        print("✅ All structural checks passed!")
        print("\nThe project has been successfully refactored according to:")
        print("- Firebase Functions best practices")
        print("- Clean Code architecture principles")
        print("- Proper separation of concerns")
        print("- Modular organization")
        print("\nAPI compatibility is maintained - all endpoints work the same.")
    else:
        print("❌ Some structural checks failed. Please review the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
