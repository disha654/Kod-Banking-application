"""
Unit tests for the login endpoint in Flask application.

Tests the POST /api/login endpoint functionality including:
- Successful login with valid credentials
- Login failure with invalid credentials
- Request validation
- Cookie setting

Requirements: 2.1, 2.5, 2.6, 2.8
"""

import unittest
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from app import app
from user_service import create_user
from db import get_connection


class TestLoginEndpoint(unittest.TestCase):
    """Test cases for the /api/login endpoint."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test client and test database."""
        cls.client = app.test_client()
        cls.client.testing = True
        
        # Clean up any existing test users
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM kodusers WHERE username LIKE 'testlogin%'")
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Setup cleanup error: {e}")
    
    def setUp(self):
        """Create a test user before each test."""
        # Create test user with known credentials
        self.test_username = f"testlogin_{datetime.utcnow().timestamp()}"
        self.test_password = "TestPass123"
        self.test_uid = f"uid_{datetime.utcnow().timestamp()}"
        self.test_email = f"{self.test_username}@test.com"
        self.test_phone = "1234567890"
        
        result = create_user(
            uid=self.test_uid,
            username=self.test_username,
            password=self.test_password,
            email=self.test_email,
            phone=self.test_phone,
            balance=100000.00
        )
        
        self.assertTrue(result['success'], "Failed to create test user")
    
    def tearDown(self):
        """Clean up test data after each test."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            # Delete test user and associated tokens
            cursor.execute("DELETE FROM CJWT WHERE uid = %s", (self.test_uid,))
            cursor.execute("DELETE FROM kodusers WHERE uid = %s", (self.test_uid,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Teardown error: {e}")
    
    def test_login_success(self):
        """Test successful login with valid credentials."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': self.test_username,
                'password': self.test_password
            }),
            content_type='application/json'
        )
        
        # Check response status and body
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Login successful')
        
        # Check that JWT cookie is set
        cookies = response.headers.getlist('Set-Cookie')
        self.assertTrue(any('jwt=' in cookie for cookie in cookies), 
                       "JWT cookie not set in response")
        
        # Verify cookie attributes
        jwt_cookie = [c for c in cookies if 'jwt=' in c][0]
        self.assertIn('HttpOnly', jwt_cookie, "Cookie should be HttpOnly")
        self.assertIn('Secure', jwt_cookie, "Cookie should be Secure")
        self.assertIn('SameSite=Strict', jwt_cookie, "Cookie should have SameSite=Strict")
        self.assertIn('Max-Age=3600', jwt_cookie, "Cookie should have Max-Age=3600")
    
    def test_login_invalid_username(self):
        """Test login with non-existent username."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': 'nonexistent_user',
                'password': 'SomePassword123'
            }),
            content_type='application/json'
        )
        
        # Check response status and body
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'INVALID_CREDENTIALS')
        self.assertIn('Invalid credentials', data['message'])
        
        # Verify no cookie is set
        cookies = response.headers.getlist('Set-Cookie')
        self.assertFalse(any('jwt=' in cookie for cookie in cookies),
                        "JWT cookie should not be set for failed login")
    
    def test_login_invalid_password(self):
        """Test login with incorrect password."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': self.test_username,
                'password': 'WrongPassword123'
            }),
            content_type='application/json'
        )
        
        # Check response status and body
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'INVALID_CREDENTIALS')
        self.assertIn('Invalid credentials', data['message'])
    
    def test_login_missing_username(self):
        """Test login with missing username field."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'password': self.test_password
            }),
            content_type='application/json'
        )
        
        # Check response status and body
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
        self.assertIn('required', data['message'].lower())
    
    def test_login_missing_password(self):
        """Test login with missing password field."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': self.test_username
            }),
            content_type='application/json'
        )
        
        # Check response status and body
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
        self.assertIn('required', data['message'].lower())
    
    def test_login_empty_username(self):
        """Test login with empty username."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': '',
                'password': self.test_password
            }),
            content_type='application/json'
        )
        
        # Check response status and body
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
    
    def test_login_empty_password(self):
        """Test login with empty password."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': self.test_username,
                'password': ''
            }),
            content_type='application/json'
        )
        
        # Check response status and body
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
    
    def test_login_missing_json_body(self):
        """Test login with no JSON body."""
        response = self.client.post(
            '/api/login',
            content_type='application/json'
        )
        
        # Check response status and body
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
        self.assertIn('JSON', data['message'])
    
    def test_login_token_stored_in_database(self):
        """Test that JWT token is stored in CJWT table after successful login."""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'username': self.test_username,
                'password': self.test_password
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify token is stored in CJWT table
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM CJWT WHERE uid = %s", (self.test_uid,))
        token_record = cursor.fetchone()
        cursor.close()
        conn.close()
        
        self.assertIsNotNone(token_record, "Token should be stored in CJWT table")
        self.assertEqual(token_record['uid'], self.test_uid)
        self.assertIsNotNone(token_record['token'])
        self.assertIsNotNone(token_record['expiry'])
        
        # Verify expiry is in the future
        self.assertGreater(token_record['expiry'], datetime.utcnow())


if __name__ == '__main__':
    unittest.main()
