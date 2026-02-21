"""
Unit tests for Flask /api/register endpoint.

Tests the registration endpoint with various scenarios including:
- Valid registration data
- Missing required fields
- Invalid field formats
- Duplicate username/email

Requirements: 1.1, 1.5, 1.6
"""

import sys
import os
import unittest
import json

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from db import execute_query, initialize_connection_pool, is_pool_initialized


class TestRegisterEndpoint(unittest.TestCase):
    """Test cases for /api/register endpoint."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test client and initialize database."""
        # Initialize database connection pool if not already initialized
        if not is_pool_initialized():
            try:
                initialize_connection_pool()
            except SystemExit:
                # Database connection failed - tests will fail but won't crash
                pass
        
        cls.client = app.test_client()
        cls.client.testing = True
    
    def setUp(self):
        """Clean up test users before each test."""
        try:
            # Delete any test users
            execute_query(
                "DELETE FROM kodusers WHERE username LIKE 'testuser%'",
                fetch=False
            )
        except Exception as e:
            print(f"Warning: Could not clean up test users: {e}")
    
    def tearDown(self):
        """Clean up test users after each test."""
        try:
            execute_query(
                "DELETE FROM kodusers WHERE username LIKE 'testuser%'",
                fetch=False
            )
        except Exception as e:
            print(f"Warning: Could not clean up test users: {e}")
    
    def test_register_valid_data(self):
        """Test registration with valid data."""
        response = self.client.post(
            '/api/register',
            data=json.dumps({
                'uid': 'testuid001',
                'uname': 'testuser001',
                'password': 'password123',
                'email': 'testuser001@example.com',
                'phone': '1234567890'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('Registration successful', data['message'])
    
    def test_register_missing_json(self):
        """Test registration without JSON body."""
        response = self.client.post('/api/register')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
    
    def test_register_missing_fields(self):
        """Test registration with missing required fields."""
        response = self.client.post(
            '/api/register',
            data=json.dumps({
                'uid': 'testuid002',
                'uname': 'testuser002',
                # Missing password, email, phone
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
    
    def test_register_invalid_email(self):
        """Test registration with invalid email format."""
        response = self.client.post(
            '/api/register',
            data=json.dumps({
                'uid': 'testuid003',
                'uname': 'testuser003',
                'password': 'password123',
                'email': 'invalid-email',
                'phone': '1234567890'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
    
    def test_register_short_password(self):
        """Test registration with password less than 8 characters."""
        response = self.client.post(
            '/api/register',
            data=json.dumps({
                'uid': 'testuid004',
                'uname': 'testuser004',
                'password': 'short',
                'email': 'testuser004@example.com',
                'phone': '1234567890'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'VALIDATION_ERROR')
    
    def test_register_duplicate_username(self):
        """Test registration with duplicate username."""
        # First registration
        self.client.post(
            '/api/register',
            data=json.dumps({
                'uid': 'testuid005',
                'uname': 'testuser005',
                'password': 'password123',
                'email': 'testuser005@example.com',
                'phone': '1234567890'
            }),
            content_type='application/json'
        )
        
        # Second registration with same username
        response = self.client.post(
            '/api/register',
            data=json.dumps({
                'uid': 'testuid006',
                'uname': 'testuser005',  # Duplicate username
                'password': 'password123',
                'email': 'testuser006@example.com',
                'phone': '1234567890'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'DUPLICATE_USER')
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email."""
        # First registration
        self.client.post(
            '/api/register',
            data=json.dumps({
                'uid': 'testuid007',
                'uname': 'testuser007',
                'password': 'password123',
                'email': 'duplicate@example.com',
                'phone': '1234567890'
            }),
            content_type='application/json'
        )
        
        # Second registration with same email
        response = self.client.post(
            '/api/register',
            data=json.dumps({
                'uid': 'testuid008',
                'uname': 'testuser008',
                'password': 'password123',
                'email': 'duplicate@example.com',  # Duplicate email
                'phone': '1234567890'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['code'], 'DUPLICATE_USER')


if __name__ == '__main__':
    unittest.main()
