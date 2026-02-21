"""
Basic tests for authentication service module.

This test file verifies the core functionality of the auth_service module.
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth_service import register_user, login, verify_token_from_request
from db import initialize_connection_pool, is_pool_initialized


def test_registration_validation():
    """Test registration input validation."""
    print("\n=== Testing Registration Validation ===")
    
    # Test missing fields
    result = register_user("", "testuser", "password123", "test@example.com", "1234567890")
    assert not result['success'], "Should fail with empty uid"
    assert result['error_code'] == 'VALIDATION_ERROR'
    print("✓ Empty uid validation works")
    
    # Test invalid email
    result = register_user("uid123", "testuser", "password123", "invalid-email", "1234567890")
    assert not result['success'], "Should fail with invalid email"
    assert result['error_code'] == 'VALIDATION_ERROR'
    print("✓ Invalid email validation works")
    
    # Test short password
    result = register_user("uid123", "testuser", "short", "test@example.com", "1234567890")
    assert not result['success'], "Should fail with short password"
    assert result['error_code'] == 'VALIDATION_ERROR'
    print("✓ Short password validation works")
    
    # Test invalid phone
    result = register_user("uid123", "testuser", "password123", "test@example.com", "123")
    assert not result['success'], "Should fail with invalid phone"
    assert result['error_code'] == 'VALIDATION_ERROR'
    print("✓ Invalid phone validation works")
    
    print("✓ All registration validation tests passed")


def test_login_validation():
    """Test login input validation."""
    print("\n=== Testing Login Validation ===")
    
    # Test missing username
    result = login("", "password123")
    assert not result['success'], "Should fail with empty username"
    assert result['error_code'] == 'VALIDATION_ERROR'
    print("✓ Empty username validation works")
    
    # Test missing password
    result = login("testuser", "")
    assert not result['success'], "Should fail with empty password"
    assert result['error_code'] == 'VALIDATION_ERROR'
    print("✓ Empty password validation works")
    
    # Test non-existent user
    result = login("nonexistentuser999", "password123")
    assert not result['success'], "Should fail with non-existent user"
    assert result['error_code'] == 'INVALID_CREDENTIALS'
    print("✓ Non-existent user validation works")
    
    print("✓ All login validation tests passed")


def test_token_verification():
    """Test token verification."""
    print("\n=== Testing Token Verification ===")
    
    # Test missing token
    result = verify_token_from_request("")
    assert not result['valid'], "Should fail with empty token"
    assert result['error_code'] == 'TOKEN_MISSING'
    print("✓ Empty token validation works")
    
    # Test invalid token
    result = verify_token_from_request("invalid.token.here")
    assert not result['valid'], "Should fail with invalid token"
    assert result['error_code'] == 'TOKEN_INVALID'
    print("✓ Invalid token validation works")
    
    print("✓ All token verification tests passed")


def main():
    """Run all tests."""
    print("Starting authentication service tests...")
    
    # Initialize database connection if not already initialized
    if not is_pool_initialized():
        print("Initializing database connection pool...")
        initialize_connection_pool()
    
    try:
        test_registration_validation()
        test_login_validation()
        test_token_verification()
        
        print("\n" + "="*50)
        print("✓ ALL TESTS PASSED")
        print("="*50)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
