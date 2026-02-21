"""
Unit tests for security headers middleware.

Tests verify that all required security headers are present in API responses.

Task 12.2: Add security headers
"""

import pytest
from unittest.mock import patch, MagicMock


# Mock the database connection before importing app
@pytest.fixture(autouse=True)
def mock_db_connection():
    """Mock database connection to avoid connection errors during testing."""
    with patch('db.initialize_connection_pool'):
        yield


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    # Import app after mocking database
    from app import app
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_security_headers_on_register_endpoint(client):
    """
    Test that security headers are present on /api/register endpoint.
    
    Verifies:
    - Content-Security-Policy header is set
    - X-Content-Type-Options header is set to 'nosniff'
    - X-Frame-Options header is set to 'DENY'
    - X-XSS-Protection header is set
    - Strict-Transport-Security header is set
    - Referrer-Policy header is set
    """
    # Make a request to register endpoint (will fail validation but headers should be present)
    response = client.post('/api/register', json={})
    
    # Verify Content-Security-Policy header
    assert 'Content-Security-Policy' in response.headers
    csp = response.headers['Content-Security-Policy']
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp
    
    # Verify X-Content-Type-Options header
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    
    # Verify X-Frame-Options header
    assert response.headers.get('X-Frame-Options') == 'DENY'
    
    # Verify X-XSS-Protection header
    assert 'X-XSS-Protection' in response.headers
    assert '1; mode=block' in response.headers['X-XSS-Protection']
    
    # Verify Strict-Transport-Security header
    assert 'Strict-Transport-Security' in response.headers
    assert 'max-age=31536000' in response.headers['Strict-Transport-Security']
    
    # Verify Referrer-Policy header
    assert 'Referrer-Policy' in response.headers


def test_security_headers_on_login_endpoint(client):
    """
    Test that security headers are present on /api/login endpoint.
    """
    # Make a request to login endpoint
    response = client.post('/api/login', json={'username': 'test', 'password': 'test'})
    
    # Verify key security headers
    assert 'Content-Security-Policy' in response.headers
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert response.headers.get('X-Frame-Options') == 'DENY'


def test_security_headers_on_balance_endpoint(client):
    """
    Test that security headers are present on /api/balance endpoint.
    """
    # Make a request to balance endpoint (will fail auth but headers should be present)
    response = client.get('/api/balance')
    
    # Verify key security headers
    assert 'Content-Security-Policy' in response.headers
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert response.headers.get('X-Frame-Options') == 'DENY'


def test_csp_header_configuration(client):
    """
    Test that Content-Security-Policy header is properly configured.
    
    Verifies CSP includes:
    - default-src 'self'
    - script-src with necessary sources
    - style-src with necessary sources
    - frame-ancestors 'none'
    """
    response = client.post('/api/register', json={})
    
    csp = response.headers.get('Content-Security-Policy', '')
    
    # Verify CSP directives
    assert "default-src 'self'" in csp
    assert "script-src" in csp
    assert "style-src" in csp
    assert "img-src" in csp
    assert "frame-ancestors 'none'" in csp


def test_additional_security_headers(client):
    """
    Test that additional security headers are present.
    
    Verifies:
    - X-DNS-Prefetch-Control
    - Permissions-Policy
    """
    response = client.post('/api/register', json={})
    
    # Verify additional security headers
    assert 'X-DNS-Prefetch-Control' in response.headers
    assert response.headers.get('X-DNS-Prefetch-Control') == 'off'
    
    assert 'Permissions-Policy' in response.headers
    permissions = response.headers.get('Permissions-Policy', '')
    assert 'geolocation=()' in permissions
    assert 'microphone=()' in permissions
    assert 'camera=()' in permissions


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
