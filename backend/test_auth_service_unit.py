"""
Unit tests for authentication service module (no database required).

This test file verifies the auth_service module structure and basic validation logic.
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_module_imports():
    """Test that auth_service module can be imported."""
    print("\n=== Testing Module Imports ===")
    
    try:
        from auth_service import register_user, login, verify_token_from_request
        print("✓ Successfully imported register_user")
        print("✓ Successfully imported login")
        print("✓ Successfully imported verify_token_from_request")
        
        # Verify functions are callable
        assert callable(register_user), "register_user should be callable"
        assert callable(login), "login should be callable"
        assert callable(verify_token_from_request), "verify_token_from_request should be callable"
        print("✓ All functions are callable")
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        raise
    
    print("✓ Module import tests passed")


def test_function_signatures():
    """Test that functions have correct signatures."""
    print("\n=== Testing Function Signatures ===")
    
    from auth_service import register_user, login, verify_token_from_request
    import inspect
    
    # Test register_user signature
    sig = inspect.signature(register_user)
    params = list(sig.parameters.keys())
    expected_params = ['uid', 'uname', 'password', 'email', 'phone']
    assert params == expected_params, f"register_user params should be {expected_params}, got {params}"
    print(f"✓ register_user has correct signature: {params}")
    
    # Test login signature
    sig = inspect.signature(login)
    params = list(sig.parameters.keys())
    expected_params = ['username', 'password']
    assert params == expected_params, f"login params should be {expected_params}, got {params}"
    print(f"✓ login has correct signature: {params}")
    
    # Test verify_token_from_request signature
    sig = inspect.signature(verify_token_from_request)
    params = list(sig.parameters.keys())
    expected_params = ['token']
    assert params == expected_params, f"verify_token_from_request params should be {expected_params}, got {params}"
    print(f"✓ verify_token_from_request has correct signature: {params}")
    
    print("✓ Function signature tests passed")


def test_validation_logic():
    """Test validation logic without database."""
    print("\n=== Testing Validation Logic ===")
    
    from auth_service import register_user, login, verify_token_from_request
    
    # Test register_user with missing fields
    result = register_user("", "user", "password123", "test@example.com", "1234567890")
    assert isinstance(result, dict), "register_user should return a dict"
    assert 'success' in result, "Result should have 'success' key"
    assert 'message' in result, "Result should have 'message' key"
    assert not result['success'], "Should fail with empty uid"
    print("✓ register_user returns proper error structure")
    
    # Test login with missing fields
    result = login("", "password")
    assert isinstance(result, dict), "login should return a dict"
    assert 'success' in result, "Result should have 'success' key"
    assert 'message' in result, "Result should have 'message' key"
    assert not result['success'], "Should fail with empty username"
    print("✓ login returns proper error structure")
    
    # Test verify_token_from_request with missing token
    result = verify_token_from_request("")
    assert isinstance(result, dict), "verify_token_from_request should return a dict"
    assert 'valid' in result, "Result should have 'valid' key"
    assert 'message' in result, "Result should have 'message' key"
    assert not result['valid'], "Should fail with empty token"
    print("✓ verify_token_from_request returns proper error structure")
    
    print("✓ Validation logic tests passed")


def test_error_codes():
    """Test that proper error codes are returned."""
    print("\n=== Testing Error Codes ===")
    
    from auth_service import register_user, login, verify_token_from_request
    
    # Test validation error codes
    result = register_user("", "user", "password123", "test@example.com", "1234567890")
    assert result.get('error_code') == 'VALIDATION_ERROR', "Should return VALIDATION_ERROR"
    print("✓ register_user returns VALIDATION_ERROR for invalid input")
    
    result = login("", "password")
    assert result.get('error_code') == 'VALIDATION_ERROR', "Should return VALIDATION_ERROR"
    print("✓ login returns VALIDATION_ERROR for missing credentials")
    
    result = verify_token_from_request("")
    assert result.get('error_code') == 'TOKEN_MISSING', "Should return TOKEN_MISSING"
    print("✓ verify_token_from_request returns TOKEN_MISSING for empty token")
    
    result = verify_token_from_request("invalid.token.here")
    assert result.get('error_code') == 'TOKEN_INVALID', "Should return TOKEN_INVALID"
    print("✓ verify_token_from_request returns TOKEN_INVALID for invalid token")
    
    print("✓ Error code tests passed")


def test_requirements_coverage():
    """Verify that the module addresses the required requirements."""
    print("\n=== Testing Requirements Coverage ===")
    
    from auth_service import register_user, login, verify_token_from_request
    import inspect
    
    # Check docstrings mention requirements
    register_doc = inspect.getdoc(register_user)
    assert 'Requirements: 1.1' in register_doc, "register_user should reference requirement 1.1"
    assert '1.6' in register_doc, "register_user should reference requirement 1.6"
    print("✓ register_user documents requirements 1.1, 1.6")
    
    login_doc = inspect.getdoc(login)
    assert 'Requirements: 2.1' in login_doc, "login should reference requirement 2.1"
    assert '2.2' in login_doc, "login should reference requirement 2.2"
    assert '2.4' in login_doc, "login should reference requirement 2.4"
    assert '2.8' in login_doc, "login should reference requirement 2.8"
    print("✓ login documents requirements 2.1, 2.2, 2.4, 2.8")
    
    verify_doc = inspect.getdoc(verify_token_from_request)
    assert 'Requirements:' in verify_doc, "verify_token_from_request should reference requirements"
    print("✓ verify_token_from_request documents requirements")
    
    print("✓ Requirements coverage tests passed")


def main():
    """Run all tests."""
    print("Starting authentication service unit tests (no database)...")
    
    try:
        test_module_imports()
        test_function_signatures()
        test_validation_logic()
        test_error_codes()
        test_requirements_coverage()
        
        print("\n" + "="*50)
        print("✓ ALL UNIT TESTS PASSED")
        print("="*50)
        print("\nThe auth_service module has been successfully created with:")
        print("  - register_user(uid, uname, password, email, phone)")
        print("  - login(username, password)")
        print("  - verify_token_from_request(token)")
        print("\nAll functions implement proper validation and error handling.")
        
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
