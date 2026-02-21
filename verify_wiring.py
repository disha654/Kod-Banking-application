"""
Verification script for Task 14.1 - Wire all components together

This script verifies that:
1. Flask app imports all endpoints correctly
2. All required modules are importable
3. All endpoints are registered
4. Configuration is properly loaded

Requirements: All
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    """Print a formatted header."""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")

def print_success(text):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    """Print info message."""
    print(f"{YELLOW}ℹ {text}{RESET}")


def verify_imports():
    """Verify all required modules can be imported."""
    print_header("STEP 1: Verify Module Imports")
    
    modules_to_test = [
        ('config', 'Configuration module'),
        ('db', 'Database connection module'),
        ('user_service', 'User service module'),
        ('jwt_service', 'JWT service module'),
        ('auth_service', 'Authentication service module'),
        ('app', 'Flask application module'),
    ]
    
    all_success = True
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print_success(f"{description} imported successfully")
        except ImportError as e:
            print_error(f"Failed to import {description}: {e}")
            all_success = False
        except Exception as e:
            print_error(f"Error importing {description}: {e}")
            all_success = False
    
    return all_success


def verify_flask_app():
    """Verify Flask app is properly configured."""
    print_header("STEP 2: Verify Flask Application")
    
    try:
        from app import app
        print_success("Flask app instance created successfully")
        
        # Check if CORS is configured
        if hasattr(app, 'extensions') and 'cors' in app.extensions:
            print_success("CORS is configured")
        else:
            print_info("CORS configuration not detected (may be configured differently)")
        
        return True
    except Exception as e:
        print_error(f"Failed to create Flask app: {e}")
        return False


def verify_endpoints():
    """Verify all required endpoints are registered."""
    print_header("STEP 3: Verify API Endpoints")
    
    try:
        from app import app
        
        # Get all registered routes
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'})),
                'path': str(rule)
            })
        
        # Required endpoints
        required_endpoints = [
            {'path': '/api/register', 'methods': 'POST', 'name': 'Registration endpoint'},
            {'path': '/api/login', 'methods': 'POST', 'name': 'Login endpoint'},
            {'path': '/api/balance', 'methods': 'GET', 'name': 'Balance endpoint'},
        ]
        
        all_found = True
        
        for required in required_endpoints:
            found = False
            for route in routes:
                if route['path'] == required['path'] and required['methods'] in route['methods']:
                    found = True
                    print_success(f"{required['name']}: {required['methods']} {required['path']}")
                    break
            
            if not found:
                print_error(f"{required['name']} not found: {required['methods']} {required['path']}")
                all_found = False
        
        # Check for frontend serving routes
        frontend_routes = [r for r in routes if r['path'] in ['/', '/<path:path>']]
        if frontend_routes:
            print_success("Frontend serving routes configured")
            for route in frontend_routes:
                print_info(f"  - {route['methods']} {route['path']}")
        else:
            print_info("Frontend serving routes not found (may need to be added)")
        
        return all_found
        
    except Exception as e:
        print_error(f"Failed to verify endpoints: {e}")
        return False


def verify_services():
    """Verify service functions are available."""
    print_header("STEP 4: Verify Service Functions")
    
    try:
        # Check auth_service functions
        from auth_service import register_user, login, verify_token_from_request
        print_success("auth_service functions available:")
        print_info("  - register_user")
        print_info("  - login")
        print_info("  - verify_token_from_request")
        
        # Check user_service functions
        from user_service import get_balance, create_user, get_user_by_username
        print_success("user_service functions available:")
        print_info("  - get_balance")
        print_info("  - create_user")
        print_info("  - get_user_by_username")
        
        # Check jwt_service functions
        from jwt_service import generate_token, validate_token, decode_token
        print_success("jwt_service functions available:")
        print_info("  - generate_token")
        print_info("  - validate_token")
        print_info("  - decode_token")
        
        # Check db functions
        from db import initialize_connection_pool, get_connection, test_connection
        print_success("db functions available:")
        print_info("  - initialize_connection_pool")
        print_info("  - get_connection")
        print_info("  - test_connection")
        
        return True
        
    except ImportError as e:
        print_error(f"Failed to import service functions: {e}")
        return False
    except Exception as e:
        print_error(f"Error verifying services: {e}")
        return False


def verify_configuration():
    """Verify configuration is properly loaded."""
    print_header("STEP 5: Verify Configuration")
    
    try:
        from config import Config
        
        # Check if environment variables are loaded
        print_info("Checking configuration...")
        
        # Check database URL
        db_config = Config.get_database_config()
        if db_config.get('url'):
            print_success("Database URL configured")
            # Don't print the actual URL for security
            print_info(f"  - URL length: {len(db_config['url'])} characters")
        else:
            print_error("Database URL not configured")
        
        # Check JWT config
        jwt_config = Config.get_jwt_config()
        if jwt_config.get('secret_key'):
            print_success("JWT secret key configured")
            print_info(f"  - Key length: {len(jwt_config['secret_key'])} characters")
        else:
            print_error("JWT secret key not configured")
        
        print_success(f"JWT expiry configured: {jwt_config.get('expiry_hours')} hours")
        print_success(f"JWT algorithm: {jwt_config.get('algorithm')}")
        
        # Check Flask config
        flask_config = Config.get_flask_config()
        print_success("Flask configuration loaded:")
        print_info(f"  - Environment: {flask_config.get('env')}")
        print_info(f"  - Debug: {flask_config.get('debug')}")
        print_info(f"  - Host: {flask_config.get('host')}")
        print_info(f"  - Port: {flask_config.get('port')}")
        
        # Check CORS config
        cors_config = Config.get_cors_config()
        print_success("CORS configuration loaded:")
        print_info(f"  - Origins: {len(cors_config.get('origins', []))} configured")
        
        # Check cookie config
        cookie_config = Config.get_cookie_config()
        print_success("Cookie configuration loaded:")
        print_info(f"  - Secure: {cookie_config.get('secure')}")
        print_info(f"  - HttpOnly: {cookie_config.get('httponly')}")
        print_info(f"  - SameSite: {cookie_config.get('samesite')}")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to verify configuration: {e}")
        return False


def verify_frontend_files():
    """Verify frontend files exist."""
    print_header("STEP 6: Verify Frontend Files")
    
    frontend_files = [
        'frontend/register.html',
        'frontend/login.html',
        'frontend/dashboard.html',
        'frontend/js/register.js',
        'frontend/js/login.js',
        'frontend/js/dashboard.js',
        'frontend/css/styles.css',
    ]
    
    all_exist = True
    
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print_success(f"{file_path} exists")
        else:
            print_error(f"{file_path} not found")
            all_exist = False
    
    return all_exist


def main():
    """Run all verification checks."""
    print_header("KODBANK1 COMPONENT WIRING VERIFICATION - Task 14.1")
    
    results = {
        'imports': verify_imports(),
        'flask_app': verify_flask_app(),
        'endpoints': verify_endpoints(),
        'services': verify_services(),
        'configuration': verify_configuration(),
        'frontend': verify_frontend_files(),
    }
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    all_passed = all(results.values())
    
    for check, passed in results.items():
        status = f"{GREEN}✓ PASSED{RESET}" if passed else f"{RED}✗ FAILED{RESET}"
        print(f"{check.upper()}: {status}")
    
    print()
    
    if all_passed:
        print_success("All components are properly wired together!")
        print_info("The application is ready for integration testing.")
        print_info("Note: Database connection requires valid credentials in .env file")
        return 0
    else:
        print_error("Some components are not properly wired.")
        print_info("Please fix the issues above before proceeding.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
