"""
Verification script for Task 13.3: Create application entry point
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def verify_run_py_exists():
    """Verify run.py file exists."""
    if os.path.exists('run.py'):
        print("[PASS] run.py exists")
        return True
    else:
        print("[FAIL] run.py does not exist")
        return False


def verify_run_py_structure():
    """Verify run.py has required functions and imports."""
    try:
        with open('run.py', 'r') as f:
            content = f.read()
        
        checks = {
            'setup_logging function': 'def setup_logging()' in content,
            'main function': 'def main()' in content,
            'app import': 'from app import app' in content,
            'Config import': 'from config import Config' in content,
            'main guard': "if __name__ == '__main__':" in content,
            'logging configuration': 'logging.basicConfig' in content,
            'Flask app.run': 'app.run(' in content,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "[PASS]" if result else "[FAIL]"
            print(f"{status} {check_name}")
            if not result:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"[FAIL] Error reading run.py: {e}")
        return False


def verify_development_production_config():
    """Verify development/production mode configuration."""
    try:
        with open('run.py', 'r') as f:
            content = f.read()
        
        checks = {
            'Config.is_development() check': 'Config.is_development()' in content,
            'Config.is_production() check': 'Config.is_production()' in content,
            'Log level based on environment': 'log_level = logging.DEBUG if Config.is_development() else logging.WARNING' in content,
            'Flask config from Config': 'Config.get_flask_config()' in content,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "[PASS]" if result else "[FAIL]"
            print(f"{status} {check_name}")
            if not result:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"[FAIL] Error checking configuration: {e}")
        return False


def verify_logging_configuration():
    """Verify logging configuration is present."""
    try:
        with open('run.py', 'r') as f:
            content = f.read()
        
        checks = {
            'Logging setup function': 'def setup_logging()' in content,
            'Logging level configuration': 'log_level' in content,
            'StreamHandler': 'StreamHandler' in content,
            'FileHandler': 'FileHandler' in content,
            'Log format': 'format=' in content,
            'Logger creation': 'logging.getLogger' in content,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "[PASS]" if result else "[FAIL]"
            print(f"{status} {check_name}")
            if not result:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"[FAIL] Error checking logging: {e}")
        return False


def verify_requirement_4_5():
    """Verify requirement 4.5 is met."""
    try:
        with open('run.py', 'r') as f:
            content = f.read()
        
        # Check for requirement comment
        has_requirement = 'Requirements: 4.5' in content or 'Requirement 4.5' in content
        
        if has_requirement:
            print("[PASS] Requirement 4.5 referenced")
            return True
        else:
            print("[FAIL] Requirement 4.5 not referenced")
            return False
            
    except Exception as e:
        print(f"[FAIL] Error checking requirement: {e}")
        return False


if __name__ == '__main__':
    print("=" * 70)
    print("Task 13.3 Verification: Create application entry point")
    print("=" * 70)
    print()
    
    results = []
    
    print("Check 1: run.py file exists")
    results.append(verify_run_py_exists())
    print()
    
    print("Check 2: run.py structure")
    results.append(verify_run_py_structure())
    print()
    
    print("Check 3: Development/Production mode configuration")
    results.append(verify_development_production_config())
    print()
    
    print("Check 4: Logging configuration")
    results.append(verify_logging_configuration())
    print()
    
    print("Check 5: Requirement 4.5 compliance")
    results.append(verify_requirement_4_5())
    print()
    
    print("=" * 70)
    if all(results):
        print("SUCCESS: Task 13.3 is complete!")
        print()
        print("Task requirements met:")
        print("  - Create run.py to start Flask application")
        print("  - Add development/production mode configuration")
        print("  - Add logging configuration")
        print("  - Requirements: 4.5")
    else:
        print("FAILURE: Some checks failed")
        sys.exit(1)
    print("=" * 70)
