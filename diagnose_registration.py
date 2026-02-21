"""
Diagnostic script to identify registration issues.
"""
import os
import sys

# Add backend to path
sys.path.insert(0, 'backend')

print("=" * 60)
print("KODBANK1 REGISTRATION DIAGNOSTIC")
print("=" * 60)

# Check environment variables
print("\n1. Checking environment variables...")
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv('DATABASE_URL')
jwt_secret = os.getenv('JWT_SECRET_KEY')

print(f"   DATABASE_URL: {'✓ Set' if db_url else '✗ Missing'}")
print(f"   JWT_SECRET_KEY: {'✓ Set' if jwt_secret else '✗ Missing'}")

if db_url and 'your_password_here' in db_url:
    print("   ⚠ WARNING: DATABASE_URL contains placeholder credentials!")
    print("   Please update .env with real AIVEN MySQL credentials")

# Check database connection
print("\n2. Testing database connection...")
try:
    from db import test_connection, initialize_connection_pool
    initialize_connection_pool()
    if test_connection():
        print("   ✓ Database connection successful")
    else:
        print("   ✗ Database connection failed")
        print("   Please check your DATABASE_URL in .env file")
except Exception as e:
    print(f"   ✗ Database connection error: {e}")
    print("   This is likely why registration is failing")

# Test user service
print("\n3. Testing user service...")
try:
    from user_service import validate_email, validate_phone, validate_username
    
    test_email = "test@example.com"
    test_phone = "1234567890"
    test_username = "testuser"
    
    print(f"   Email validation ({test_email}): {'✓' if validate_email(test_email) else '✗'}")
    print(f"   Phone validation ({test_phone}): {'✓' if validate_phone(test_phone) else '✗'}")
    print(f"   Username validation ({test_username}): {'✓' if validate_username(test_username) else '✗'}")
    
except Exception as e:
    print(f"   ✗ User service error: {e}")

# Test registration flow
print("\n4. Testing registration flow...")
try:
    from auth_service import register_user
    
    test_data = {
        'uid': 'TEST001',
        'uname': 'diagtest',
        'password': 'testpass123',
        'email': 'diagtest@example.com',
        'phone': '1234567890'
    }
    
    print(f"   Attempting registration with test data...")
    result = register_user(**test_data)
    
    if result['success']:
        print(f"   ✓ Registration successful: {result['message']}")
    else:
        print(f"   ✗ Registration failed: {result['message']}")
        print(f"   Error code: {result.get('error_code', 'N/A')}")
        
except Exception as e:
    print(f"   ✗ Registration error: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    print("\n   Full traceback:")
    traceback.print_exc()

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
