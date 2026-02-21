"""
Manual test script for user_service module.

This script tests the basic functionality of the user service.
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import initialize_connection_pool
from user_service import (
    create_user,
    get_user_by_username,
    user_exists,
    get_balance,
    hash_password,
    verify_password,
    validate_email,
    validate_phone,
    validate_username,
    validate_uid,
    validate_password
)


def test_validation_functions():
    """Test input validation functions."""
    print("\n=== Testing Validation Functions ===")
    
    # Test email validation
    assert validate_email("test@example.com") == True
    assert validate_email("invalid-email") == False
    assert validate_email("") == False
    print("✓ Email validation works")
    
    # Test phone validation
    assert validate_phone("1234567890") == True
    assert validate_phone("+1 (555) 123-4567") == True
    assert validate_phone("123") == False
    print("✓ Phone validation works")
    
    # Test username validation
    assert validate_username("john_doe123") == True
    assert validate_username("user@name") == False
    assert validate_username("a" * 51) == False
    print("✓ Username validation works")
    
    # Test UID validation
    assert validate_uid("user123") == True
    assert validate_uid("") == False
    assert validate_uid("a" * 51) == False
    print("✓ UID validation works")
    
    # Test password validation
    assert validate_password("password123") == True
    assert validate_password("short") == False
    print("✓ Password validation works")


def test_password_hashing():
    """Test password hashing and verification."""
    print("\n=== Testing Password Hashing ===")
    
    password = "mySecurePassword123"
    
    # Hash the password
    hashed = hash_password(password)
    print(f"✓ Password hashed: {hashed[:20]}...")
    
    # Verify correct password
    assert verify_password(password, hashed) == True
    print("✓ Correct password verification works")
    
    # Verify incorrect password
    assert verify_password("wrongPassword", hashed) == False
    print("✓ Incorrect password rejection works")
    
    # Verify different hashes for same password
    hashed2 = hash_password(password)
    assert hashed != hashed2
    print("✓ Different hashes generated for same password (salt working)")


def test_user_operations():
    """Test user CRUD operations."""
    print("\n=== Testing User Operations ===")
    
    # Initialize database connection
    print("Initializing database connection...")
    initialize_connection_pool()
    print("✓ Database connection initialized")
    
    # Test user creation
    test_user = {
        'uid': 'test_user_001',
        'username': 'testuser',
        'password': 'testPassword123',
        'email': 'test@example.com',
        'phone': '1234567890'
    }
    
    print(f"\nCreating test user: {test_user['username']}")
    result = create_user(
        uid=test_user['uid'],
        username=test_user['username'],
        password=test_user['password'],
        email=test_user['email'],
        phone=test_user['phone']
    )
    
    if result['success']:
        print(f"✓ User created: {result['message']}")
    else:
        print(f"⚠ User creation result: {result['message']}")
    
    # Test user_exists
    print(f"\nChecking if user exists...")
    exists = user_exists(username=test_user['username'])
    assert exists == True
    print(f"✓ User exists check works: {exists}")
    
    # Test get_user_by_username
    print(f"\nRetrieving user by username...")
    user = get_user_by_username(test_user['username'])
    assert user is not None
    assert user['username'] == test_user['username']
    assert user['email'] == test_user['email']
    print(f"✓ User retrieved: {user['username']}")
    
    # Verify password is hashed
    assert user['password'] != test_user['password']
    assert user['password'].startswith('$2b$')
    print(f"✓ Password is hashed in database")
    
    # Test password verification
    is_valid = verify_password(test_user['password'], user['password'])
    assert is_valid == True
    print(f"✓ Password verification works")
    
    # Test get_balance
    print(f"\nRetrieving user balance...")
    balance = get_balance(test_user['username'])
    assert balance == 100000.00
    print(f"✓ Balance retrieved: {balance}")
    
    # Test duplicate user creation
    print(f"\nAttempting to create duplicate user...")
    result = create_user(
        uid='test_user_002',
        username=test_user['username'],
        password='anotherPassword123',
        email='another@example.com',
        phone='9876543210'
    )
    assert result['success'] == False
    print(f"✓ Duplicate username rejected: {result['message']}")
    
    # Test duplicate email
    print(f"\nAttempting to create user with duplicate email...")
    result = create_user(
        uid='test_user_003',
        username='anotheruser',
        password='anotherPassword123',
        email=test_user['email'],
        phone='9876543210'
    )
    assert result['success'] == False
    print(f"✓ Duplicate email rejected: {result['message']}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("User Service Module Test")
    print("=" * 60)
    
    try:
        # Test validation functions (no DB required)
        test_validation_functions()
        
        # Test password hashing (no DB required)
        test_password_hashing()
        
        # Test user operations (requires DB)
        test_user_operations()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
