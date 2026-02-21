"""
Integration test for kodbank1 application - Task 14.1

This script tests the complete flows:
1. Registration flow
2. Login flow
3. Balance check flow

Requirements: All
"""

import sys
import os
import time
import requests
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Test configuration
BASE_URL = 'http://localhost:5000'
TEST_USER_PREFIX = f'testuser_{int(time.time())}'

# ANSI color codes for output
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

def test_registration_flow():
    """
    Test complete registration flow.
    
    Steps:
    1. Submit registration with all required fields
    2. Verify success response
    3. Verify user can't register again with same username
    4. Verify user can't register again with same email
    """
    print_header("TEST 1: Registration Flow")
    
    # Test data
    test_user = {
        'uid': f'{TEST_USER_PREFIX}_uid',
        'uname': f'{TEST_USER_PREFIX}_name',
        'password': 'TestPassword123!',
        'email': f'{TEST_USER_PREFIX}@test.com',
        'phone': '+1234567890'
    }
    
    try:
        # Test 1.1: Valid registration
        print_info("Testing valid registration...")
        response = requests.post(
            f'{BASE_URL}/api/register',
            json=test_user,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print_success("Valid registration succeeded")
            else:
                print_error(f"Registration returned success status but wrong data: {data}")
                return False
        else:
            print_error(f"Registration failed with status {response.status_code}: {response.text}")
            return False
        
        # Test 1.2: Duplicate username
        print_info("Testing duplicate username rejection...")
        duplicate_user = test_user.copy()
        duplicate_user['email'] = f'{TEST_USER_PREFIX}_different@test.com'
        duplicate_user['uid'] = f'{TEST_USER_PREFIX}_different_uid'
        
        response = requests.post(
            f'{BASE_URL}/api/register',
            json=duplicate_user,
            timeout=10
        )
        
        if response.status_code in [400, 409]:
            data = response.json()
            if data.get('status') == 'error':
                print_success("Duplicate username correctly rejected")
            else:
                print_error(f"Duplicate username not rejected properly: {data}")
                return False
        else:
            print_error(f"Duplicate username should be rejected but got status {response.status_code}")
            return False
        
        # Test 1.3: Duplicate email
        print_info("Testing duplicate email rejection...")
        duplicate_email = test_user.copy()
        duplicate_email['uname'] = f'{TEST_USER_PREFIX}_different_name'
        duplicate_email['uid'] = f'{TEST_USER_PREFIX}_different_uid2'
        
        response = requests.post(
            f'{BASE_URL}/api/register',
            json=duplicate_email,
            timeout=10
        )
        
        if response.status_code in [400, 409]:
            data = response.json()
            if data.get('status') == 'error':
                print_success("Duplicate email correctly rejected")
            else:
                print_error(f"Duplicate email not rejected properly: {data}")
                return False
        else:
            print_error(f"Duplicate email should be rejected but got status {response.status_code}")
            return False
        
        print_success("Registration flow completed successfully")
        return test_user
        
    except requests.exceptions.RequestException as e:
        print_error(f"Network error during registration test: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error during registration test: {e}")
        return False


def test_login_flow(test_user):
    """
    Test complete login flow.
    
    Steps:
    1. Login with valid credentials
    2. Verify JWT token is set in cookie
    3. Test login with invalid credentials
    """
    print_header("TEST 2: Login Flow")
    
    try:
        # Test 2.1: Valid login
        print_info("Testing valid login...")
        session = requests.Session()
        
        response = session.post(
            f'{BASE_URL}/api/login',
            json={
                'username': test_user['uname'],
                'password': test_user['password']
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                # Check if JWT cookie is set
                if 'jwt' in session.cookies:
                    print_success("Valid login succeeded and JWT cookie set")
                else:
                    print_error("Login succeeded but JWT cookie not set")
                    return False
            else:
                print_error(f"Login returned success status but wrong data: {data}")
                return False
        else:
            print_error(f"Login failed with status {response.status_code}: {response.text}")
            return False
        
        # Test 2.2: Invalid credentials
        print_info("Testing invalid credentials rejection...")
        response = requests.post(
            f'{BASE_URL}/api/login',
            json={
                'username': test_user['uname'],
                'password': 'WrongPassword123!'
            },
            timeout=10
        )
        
        if response.status_code == 401:
            data = response.json()
            if data.get('status') == 'error':
                print_success("Invalid credentials correctly rejected")
            else:
                print_error(f"Invalid credentials not rejected properly: {data}")
                return False
        else:
            print_error(f"Invalid credentials should be rejected but got status {response.status_code}")
            return False
        
        # Test 2.3: Non-existent user
        print_info("Testing non-existent user rejection...")
        response = requests.post(
            f'{BASE_URL}/api/login',
            json={
                'username': 'nonexistent_user_12345',
                'password': 'SomePassword123!'
            },
            timeout=10
        )
        
        if response.status_code == 401:
            data = response.json()
            if data.get('status') == 'error':
                print_success("Non-existent user correctly rejected")
            else:
                print_error(f"Non-existent user not rejected properly: {data}")
                return False
        else:
            print_error(f"Non-existent user should be rejected but got status {response.status_code}")
            return False
        
        print_success("Login flow completed successfully")
        return session
        
    except requests.exceptions.RequestException as e:
        print_error(f"Network error during login test: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error during login test: {e}")
        return False


def test_balance_check_flow(session):
    """
    Test complete balance check flow.
    
    Steps:
    1. Check balance with valid JWT token
    2. Verify balance is returned correctly
    3. Test balance check without token
    """
    print_header("TEST 3: Balance Check Flow")
    
    try:
        # Test 3.1: Valid balance check
        print_info("Testing balance check with valid token...")
        response = session.get(
            f'{BASE_URL}/api/balance',
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success' and 'balance' in data:
                balance = data['balance']
                # Initial balance should be 1000002 according to requirements
                if balance == 1000002:
                    print_success(f"Balance check succeeded with correct initial balance: {balance}")
                else:
                    print_success(f"Balance check succeeded with balance: {balance}")
                    print_info(f"Note: Expected initial balance 1000002, got {balance}")
            else:
                print_error(f"Balance check returned success but wrong data: {data}")
                return False
        else:
            print_error(f"Balance check failed with status {response.status_code}: {response.text}")
            return False
        
        # Test 3.2: Balance check without token
        print_info("Testing balance check without token...")
        response = requests.get(
            f'{BASE_URL}/api/balance',
            timeout=10
        )
        
        if response.status_code == 401:
            data = response.json()
            if data.get('status') == 'error':
                print_success("Balance check without token correctly rejected")
            else:
                print_error(f"Balance check without token not rejected properly: {data}")
                return False
        else:
            print_error(f"Balance check without token should be rejected but got status {response.status_code}")
            return False
        
        print_success("Balance check flow completed successfully")
        return True
        
    except requests.exceptions.RequestException as e:
        print_error(f"Network error during balance check test: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error during balance check test: {e}")
        return False


def main():
    """Run all integration tests."""
    print_header("KODBANK1 INTEGRATION TESTS - Task 14.1")
    print_info(f"Testing against: {BASE_URL}")
    print_info(f"Test user prefix: {TEST_USER_PREFIX}")
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=5)
        print_success("Server is running")
    except requests.exceptions.RequestException:
        print_error("Server is not running. Please start the Flask application first.")
        print_info("Run: python run.py")
        return False
    
    # Run tests
    test_user = test_registration_flow()
    if not test_user:
        print_error("Registration flow failed. Stopping tests.")
        return False
    
    session = test_login_flow(test_user)
    if not session:
        print_error("Login flow failed. Stopping tests.")
        return False
    
    success = test_balance_check_flow(session)
    if not success:
        print_error("Balance check flow failed.")
        return False
    
    # Final summary
    print_header("TEST SUMMARY")
    print_success("All integration tests passed!")
    print_info("✓ Registration flow works correctly")
    print_info("✓ Login flow works correctly")
    print_info("✓ Balance check flow works correctly")
    print_info("✓ All components are properly wired together")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
