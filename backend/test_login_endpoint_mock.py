"""
Mock-based unit tests for the login endpoint in Flask application.

Tests the POST /api/login endpoint functionality with mocked dependencies:
- Successful login with valid credentials
- Login failure with invalid credentials
- Request validation
- Cookie setting

Requirements: 2.1, 2.5, 2.6, 2.8
"""

import unittest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime


class TestLoginEndpointMocked(unittest.TestCase):
    """Test cases for the /api/login endpoint with mocked dependencies."""
    
    def setUp(self):
        """Set up test client."""
        # Import app here to avoid database connection on module load
        with patch('app.initialize_connection_pool'):
            from app import app
            self.app = app
            self.client = app.test_client()
            self.client.testing = True
    
    @patch('app.login')
    def test_login_success_with_cookie(self, mock_login):
        """Test successful login returns success response and sets cookie."""
        # Mock successful login
        mock_login.return_value = {
            'success': True,
            'message': 'Login successful',
            'token': 'mock.jwt.token',
            'uid': 'test_uid_123'
        }
        
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'TestPass123'
            }),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Login successful')
        
        # Verify login was called with correct arguments
        mock_login.assert_called_once_with(username='testuser', password='TestPass123')
        
        # Verify JWT cookie is set with correct attributes
        cookies = response.headers.getlist('Set-Cookie')
        self.assertTrue(any('jwt=' in cookie for cookie in cookies), 
                       "JWT cookie not set in response")
        
        jwt_cookie = [c for c in cookies if 'jwt=' in c][0]
        self.assertIn('jwt=mock.jwt.token', jwt_cookie)
        self.assertIn('HttpOnly', jwt_cookie, "Cookie should be HttpOnly")
        self.assertIn('Secure', jwt_cookie, "Cookie should be Secure")
        self.assertIn('SameSite=Strict', jwt_cookie, "Cookie should have SameSite=Strict")
        self.assertIn('Max-Age=3600', jwt_cookie, "Cookie should have Max-Age=3600")
    
    @patch('app.login')
    def test_login_invalid_credentials(self, mock_login):
        """Test login with invalid credentials returns 401 error."""
        # Mock failed login
        mock_login.return_value = {
            'success': False,
            'message': 'Invalid credentials',
            'error_code': 'INVALID_CREDENTIALS'
        }
        
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'WrongPassword'
            }),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'INVALID_CREDENTIALS')
        self.assertIn('Invalid credentials', data['message'])
        self.assertIn('timestamp', data)
        
        # Verify no cookie is set
        cookies = response.headers.getlist('Set-Cookie')
        self.assertFalse(any('jwt=' in cookie for cookie in cookies),
                        "JWT cookie should not be set for failed login")
    
    @patch('app.login')
    def test_login_missing_username(self, mock_login):
        """Test login with missing username returns validation error."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'password': 'TestPass123'
            }),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
        self.assertIn('required', data['message'].lower())
        
        # Verify login was not called
        mock_login.assert_not_called()
    
    @patch('app.login')
    def test_login_missing_password(self, mock_login):
        """Test login with missing password returns validation error."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': 'testuser'
            }),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
        self.assertIn('required', data['message'].lower())
        
        # Verify login was not called
        mock_login.assert_not_called()
    
    @patch('app.login')
    def test_login_empty_username(self, mock_login):
        """Test login with empty username returns validation error."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': '',
                'password': 'TestPass123'
            }),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
        
        # Verify login was not called
        mock_login.assert_not_called()
    
    @patch('app.login')
    def test_login_empty_password(self, mock_login):
        """Test login with empty password returns validation error."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': 'testuser',
                'password': ''
            }),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
        
        # Verify login was not called
        mock_login.assert_not_called()
    
    @patch('app.login')
    def test_login_missing_json_body(self, mock_login):
        """Test login with no JSON body returns validation error."""
        response = self.client.post(
            '/api/login',
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
        self.assertIn('JSON', data['message'])
        
        # Verify login was not called
        mock_login.assert_not_called()
    
    @patch('app.login')
    def test_login_validation_error(self, mock_login):
        """Test login with validation error from auth service."""
        # Mock validation error
        mock_login.return_value = {
            'success': False,
            'message': 'Username and password are required',
            'error_code': 'VALIDATION_ERROR'
        }
        
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'pass'
            }),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
    
    @patch('app.login')
    def test_login_internal_error(self, mock_login):
        """Test login handles internal errors gracefully."""
        # Mock internal error
        mock_login.side_effect = Exception("Database connection failed")
        
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': 'testuser',
                'password': 'TestPass123'
            }),
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'INTERNAL_ERROR')
        self.assertIn('Internal server error', data['message'])


if __name__ == '__main__':
    unittest.main()
