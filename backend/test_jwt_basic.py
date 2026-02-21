"""
Basic unit tests for JWT service module (without database).

Tests JWT token generation, validation, and decoding without database dependency.
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
    JWT_EXPIRY_HOURS
)
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
        print(f"  Payload: {payload}")
        
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
        iat_time = datetime.fromtimestamp(payload['iat'])
        now = datetime.utcnow()
        assert exp_time > iat_time, "Expiration should be after issued time"
        print(f"✓ Expiration is after issued time")
        
        # Verify expiration is approximately 1 hour after issued time
        time_diff = (payload['exp'] - payload['iat'])
        expected_seconds = JWT_EXPIRY_HOURS * 3600
        assert abs(time_diff - expected_seconds) < 10, f"Expiration should be {JWT_EXPIRY_HOURS} hour(s) after issued time"
        print(f"✓ Expiration is set to {JWT_EXPIRY_HOURS} hour(s) from issued time")
        
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


def test_token_signature_validation():
    """Test that tokens with invalid signatures are rejected."""
    print("\n=== Test: Token Signature Validation ===")
    
    try:
        # Generate a valid token
        valid_token = generate_token('signaturetest', 'customer')
        
        # Tamper with the token (change last character)
        tampered_token = valid_token[:-1] + ('a' if valid_token[-1] != 'a' else 'b')
        
        # Validate tampered token
        is_valid = validate_token(tampered_token)
        assert is_valid == False, "Tampered token should fail validation"
        print(f"✓ Tampered token fails validation")
        
        # Decode tampered token
        payload = decode_token(tampered_token)
        assert payload is None, "Tampered token should return None when decoded"
        print(f"✓ Tampered token returns None when decoded")
        
    except Exception as e:
        print(f"✗ Token signature validation test failed: {e}")
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


def test_multiple_users():
    """Test generating tokens for different users."""
    print("\n=== Test: Multiple Users ===")
    
    try:
        # Generate tokens for different users
        token1 = generate_token('user1', 'customer')
        token2 = generate_token('user2', 'customer')
        token3 = generate_token('admin', 'admin')
        
        # Decode and verify each token
        payload1 = decode_token(token1)
        payload2 = decode_token(token2)
        payload3 = decode_token(token3)
        
        assert payload1['sub'] == 'user1', "Token 1 should have correct username"
        assert payload2['sub'] == 'user2', "Token 2 should have correct username"
        assert payload3['sub'] == 'admin', "Token 3 should have correct username"
        print(f"✓ Multiple user tokens have correct usernames")
        
        assert payload1['role'] == 'customer', "Token 1 should have customer role"
        assert payload2['role'] == 'customer', "Token 2 should have customer role"
        assert payload3['role'] == 'admin', "Token 3 should have admin role"
        print(f"✓ Multiple user tokens have correct roles")
        
        # Verify tokens are different
        assert token1 != token2, "Tokens for different users should be different"
        assert token2 != token3, "Tokens for different users should be different"
        print(f"✓ Tokens for different users are unique")
        
    except Exception as e:
        print(f"✗ Multiple users test failed: {e}")
        raise


def run_all_tests():
    """Run all JWT service tests."""
    print("=" * 60)
    print("JWT Service Basic Unit Tests")
    print("=" * 60)
    
    try:
        # Run tests
        token = test_token_generation()
        test_token_structure(token)
        test_token_validation()
        test_token_signature_validation()
        test_token_expiration()
        test_multiple_users()
        
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
