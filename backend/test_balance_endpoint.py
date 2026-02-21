"""
Test suite for the balance endpoint.

This test verifies the GET /api/balance endpoint implementation.

Requirements: 3.2, 3.3, 3.4, 3.5, 3.6, 3.9
"""

import pytest
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from auth_service import register_user, login
from db import execute_query


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_user():
    """Create a test user and return credentials."""
    # Clean up any existing test user
    try:
        execute_query("DELETE FROM kodusers WHERE username = %s", ('testbalanceuser',), fetch=False)
        execute_query("DELETE FROM CJWT WHERE uid = %s", ('testbalance123',), fetch=False)
    except:
        pass
    
    # Register test user
    user_data = {
        'uid': 'testbalance123',
        'uname': 'testbalanceuser',
        'password': 'testpass123',
        'email': 'testbalance@example.com',
        'phone': '1234567890'
    }
    
    register_result = register_user(**user_data)
    assert register_result['success'], "Test user registration failed"
    
    yield user_data
    
    # Cleanup
    try:
        execute_query("DELETE FROM kodusers WHERE username = %s", ('testbalanceuser',), fetch=False)
        execute_query("DELETE FROM CJWT WHERE uid = %s", ('testbalance123',), fetch=False)
    except:
        pass


def test_balance_with_valid_token(client, test_user):
    """Test balance retrieval with valid JWT token."""
    # Login to get JWT token
    login_response = client.post('/api/login', json={
        'username': test_user['uname'],
        'password': test_user['password']
    })
    
    assert login_response.status_code == 200
    assert 'jwt' in login_response.headers.get('Set-Cookie', '')
    
    # Request balance with cookie
    balance_response = client.get('/api/balance')
    
    assert balance_response.status_code == 200
    data = balance_response.get_json()
    assert data['status'] == 'success'
    assert 'balance' in data
    assert data['balance'] == 100000.00  # Initial balance


def test_balance_without_token(client):
    """Test balance request without JWT token."""
    balance_response = client.get('/api/balance')
    
    assert balance_response.status_code == 401
    data = balance_response.get_json()
    assert data['status'] == 'error'
    assert data['code'] == 'TOKEN_MISSING'


def test_balance_with_invalid_token(client):
    """Test balance request with invalid JWT token."""
    # Set invalid token in cookie
    client.set_cookie('jwt', 'invalid.token.here')
    
    balance_response = client.get('/api/balance')
    
    assert balance_response.status_code == 401
    data = balance_response.get_json()
    assert data['status'] == 'error'
    assert data['code'] == 'TOKEN_INVALID'


def test_balance_with_malformed_token(client):
    """Test balance request with malformed JWT token."""
    # Set malformed token in cookie
    client.set_cookie('jwt', 'not-a-jwt-token')
    
    balance_response = client.get('/api/balance')
    
    assert balance_response.status_code == 401
    data = balance_response.get_json()
    assert data['status'] == 'error'
    assert data['code'] == 'TOKEN_INVALID'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
