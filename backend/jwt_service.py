"""
JWT service module for kodbank1 application.

This module provides JWT token management functionality including:
- JWT token generation with username and role claims
- Token signature validation
- Token expiration checking
- Token storage and retrieval from database

Requirements: 2.2, 2.3, 2.4, 5.1, 5.2, 5.3, 5.4
"""

import os
import logging
from datetime import datetime, timedelta
import jwt
from mysql.connector import Error
from db import execute_query
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRY_HOURS = int(os.getenv('JWT_EXPIRY_HOURS', 1))


def generate_token(username, role='customer'):
    """
    Generate a JWT token with username as subject and role as claim.
    
    Args:
        username (str): Username to include as subject
        role (str, optional): User role to include as claim (default: 'customer')
        
    Returns:
        str: JWT token string
        
    Raises:
        ValueError: If username is empty or JWT_SECRET_KEY is not configured
    """
    if not username:
        raise ValueError("Username is required for token generation")
    
    if not JWT_SECRET_KEY:
        logger.error("JWT_SECRET_KEY not configured")
        raise ValueError("JWT_SECRET_KEY environment variable is required")
    
    try:
        # Calculate expiration time (1 hour from now)
        issued_at = datetime.utcnow()
        expiration = issued_at + timedelta(hours=JWT_EXPIRY_HOURS)
        
        # Create token payload
        payload = {
            'sub': username,           # Subject: username
            'role': role,              # Role claim
            'iat': issued_at,          # Issued at
            'exp': expiration          # Expiration
        }
        
        # Generate and sign token
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        
        logger.info(f"JWT token generated for user: {username}")
        return token
        
    except Exception as e:
        logger.error(f"Error generating JWT token: {e}")
        raise


def validate_token(token):
    """
    Validate JWT token signature and expiration.
    
    Args:
        token (str): JWT token to validate
        
    Returns:
        bool: True if token is valid and not expired, False otherwise
    """
    if not token:
        return False
    
    if not JWT_SECRET_KEY:
        logger.error("JWT_SECRET_KEY not configured")
        return False
    
    try:
        # Decode and verify token
        # This will raise an exception if signature is invalid or token is expired
        jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return True
        
    except jwt.ExpiredSignatureError:
        logger.warning("Token validation failed: token expired")
        return False
    except jwt.InvalidTokenError as e:
        logger.warning(f"Token validation failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error validating token: {e}")
        return False


def decode_token(token):
    """
    Decode JWT token and return payload.
    
    Args:
        token (str): JWT token to decode
        
    Returns:
        dict or None: Token payload if valid, None if invalid or expired
    """
    if not token:
        return None
    
    if not JWT_SECRET_KEY:
        logger.error("JWT_SECRET_KEY not configured")
        return None
    
    try:
        # Decode and verify token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
        
    except jwt.ExpiredSignatureError:
        logger.warning("Token decode failed: token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Token decode failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {e}")
        return None


def store_token(token, uid, expiry):
    """
    Store JWT token in CJWT table with expiry time.
    
    Args:
        token (str): JWT token to store
        uid (str): User ID associated with the token
        expiry (datetime): Token expiration timestamp
        
    Returns:
        dict: Result dictionary with 'success' (bool) and 'message' (str)
        
    Raises:
        ValueError: If required parameters are missing
    """
    if not token:
        raise ValueError("Token is required")
    
    if not uid:
        raise ValueError("User ID is required")
    
    if not expiry:
        raise ValueError("Expiry time is required")
    
    try:
        query = """
            INSERT INTO cjwt (token, uid, expiry)
            VALUES (%s, %s, %s)
        """
        params = (token, uid, expiry)
        
        execute_query(query, params, fetch=False)
        
        logger.info(f"Token stored successfully for user: {uid}")
        return {
            'success': True,
            'message': 'Token stored successfully'
        }
        
    except Error as e:
        logger.error(f"Database error storing token: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error storing token: {e}")
        raise


def token_exists(token):
    """
    Check if a token exists in the CJWT table.
    
    Args:
        token (str): JWT token to check
        
    Returns:
        bool: True if token exists, False otherwise
    """
    if not token:
        return False
    
    try:
        query = "SELECT COUNT(*) as count FROM cjwt WHERE token = %s"
        params = (token,)
        
        results = execute_query(query, params, fetch=True)
        return results[0]['count'] > 0
        
    except Error as e:
        logger.error(f"Error checking token existence: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error checking token existence: {e}")
        raise
