"""
Unit tests for JWT service module.

Tests JWT token generation, validation, decoding, storage, and existence checking.
"""

import sys
import os
from datetime import datetime, timedelta

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jwt_service import (
    generate_token,
    validate_token,
    decode_token,
    store_token,
    token_exists
)
from db import initialize_connection_pool
import jwt


def test_token_generation():
    """Test JWT token generation with username and role."""
    print("\n=== Test: Token Generation ===")
    
    try:
        # Generate token
        token = generate_token('testuser', 'customer')
        print(f"✓ Token generated successfully")
        print(f"  Token (first 50 chars): {token[:50]}...")
        
        # Verify token is a string
        assert isinstance(token, str), "Token should be a string"
        assert len(token) > 0, "Token should not be empty"
        print(f"✓ Token is valid string")
        
        return token
        
    except Exception as e:
        print(f"✗ Token generation failed: {e}")
        raise


def test_token_structure(token):
    """Test that token contains correct claims."""
    print("\n=== Test: Token Structure ===")
    
    try:
        # Decode token payload
        payload = decode_token(token)
        
        assert payload is not None, "Payload should not be None"
        print(f"✓ Token decoded successfully")
        
        # Check required claims
        assert 'sub' in payload, "Token should contain 'sub' claim"
        assert payload['sub'] == 'testuser', "Subject should be 'testuser'"
        print(f"✓ Subject claim correct: {payload['sub']}")
        
        assert 'role' in payload, "Token should contain 'role' claim"
        assert payload['role'] == 'customer', "Role should be 'customer'"
        print(f"✓ Role claim correct: {payload['role']}")
        
        assert 'iat' in payload, "Token should contain 'iat' claim"
        print(f"✓ Issued at claim present")
        
        assert 'exp' in payload, "Token should contain 'exp' claim"
        print(f"✓ Expiration claim present")
        
        # Verify expiration is in the future
        exp_time = datetime.fromtimestamp(payload['exp'])
        now = datetime.utcnow()
        assert exp_time > now, "Expiration should be in the future"
        print(f"✓ Expiration is in the future: {exp_time}")
        
    except Exception as e:
        print(f"✗ Token structure test failed: {e}")
        raise


def test_token_validation():
    """Test token validation with valid and invalid tokens."""
    print("\n=== Test: Token Validation ===")
    
    try:
        # Test valid token
        valid_token = generate_token('validuser', 'customer')
        is_valid = validate_token(valid_token)
        assert is_valid == True, "Valid token should pass validation"
        print(f"✓ Valid token passes validation")
        
        # Test invalid token (malformed)
        invalid_token = "invalid.token.here"
        is_valid = validate_token(invalid_token)
        assert is_valid == False, "Invalid token should fail validation"
        print(f"✓ Invalid token fails validation")
        
        # Test empty token
        is_valid = validate_token("")
        assert is_valid == False, "Empty token should fail validation"
        print(f"✓ Empty token fails validation")
        
        # Test None token
        is_valid = validate_token(None)
        assert is_valid == False, "None token should fail validation"
        print(f"✓ None token fails validation")
        
    except Exception as e:
        print(f"✗ Token validation test failed: {e}")
        raise


def test_token_expiration():
    """Test that expired tokens are rejected."""
    print("\n=== Test: Token Expiration ===")
    
    try:
        # Create an expired token manually
        from jwt_service import JWT_SECRET_KEY, JWT_ALGORITHM
        
        past_time = datetime.utcnow() - timedelta(hours=2)
        expired_payload = {
            'sub': 'expireduser',
            'role': 'customer',
            'iat': past_time,
            'exp': past_time + timedelta(seconds=1)  # Expired 2 hours ago
        }
        
        expired_token = jwt.encode(expired_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        # Validate expired token
        is_valid = validate_token(expired_token)
        assert is_valid == False, "Expired token should fail validation"
        print(f"✓ Expired token fails validation")
        
        # Decode expired token
        payload = decode_token(expired_token)
        assert payload is None, "Expired token should return None when decoded"
        print(f"✓ Expired token returns None when decoded")
        
    except Exception as e:
        print(f"✗ Token expiration test failed: {e}")
        raise


def test_token_storage():
    """Test storing token in database."""
    print("\n=== Test: Token Storage ===")
    
    try:
        # Generate a token
        token = generate_token('storageuser', 'customer')
        
        # Calculate expiry
        expiry = datetime.utcnow() + timedelta(hours=1)
        
        # Store token
        result = store_token(token, 'test_uid_123', expiry)
        
        assert result['success'] == True, "Token storage should succeed"
        print(f"✓ Token stored successfully")
        print(f"  Message: {result['message']}")
        
        return token
        
    except Exception as e:
        print(f"✗ Token storage test failed: {e}")
        raise


def test_token_exists_check(stored_token):
    """Test checking if token exists in database."""
    print("\n=== Test: Token Existence Check ===")
    
    try:
        # Check if stored token exists
        exists = token_exists(stored_token)
        assert exists == True, "Stored token should exist"
        print(f"✓ Stored token exists in database")
        
        # Check if non-existent token exists
        fake_token = "fake.token.that.does.not.exist"
        exists = token_exists(fake_token)
        assert exists == False, "Non-existent token should not exist"
        print(f"✓ Non-existent token correctly returns False")
        
        # Check empty token
        exists = token_exists("")
        assert exists == False, "Empty token should return False"
        print(f"✓ Empty token returns False")
        
    except Exception as e:
        print(f"✗ Token existence check failed: {e}")
        raise


def run_all_tests():
    """Run all JWT service tests."""
    print("=" * 60)
    print("JWT Service Unit Tests")
    print("=" * 60)
    
    try:
        # Initialize database connection
        print("\nInitializing database connection...")
        initialize_connection_pool()
        print("✓ Database connection initialized")
        
        # Run tests
        token = test_token_generation()
        test_token_structure(token)
        test_token_validation()
        test_token_expiration()
        stored_token = test_token_storage()
        test_token_exists_check(stored_token)
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ Tests failed: {e}")
        print("=" * 60)
        raise


if __name__ == '__main__':
    run_all_tests()
