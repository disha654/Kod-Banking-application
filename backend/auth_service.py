"""
Authentication service module for kodbank1 application.

This module provides authentication functionality including:
- User registration with validation and duplicate checking
- User login with credential validation and JWT generation
- Token extraction and verification from HTTP requests

Requirements: 1.1, 1.6, 2.1, 2.2, 2.4, 2.8
"""

import logging
from datetime import datetime, timedelta
from user_service import (
    create_user,
    get_user_by_username,
    verify_password,
    validate_uid,
    validate_username,
    validate_password,
    validate_email,
    validate_phone
)
from jwt_service import (
    generate_token,
    validate_token,
    decode_token,
    store_token
)

# Configure logging
logger = logging.getLogger(__name__)


def register_user(uid, uname, password, email, phone):
    """
    Register a new user with validation and duplicate checking.
    
    This function performs the complete registration flow:
    1. Validates all required fields are provided
    2. Validates field formats
    3. Checks for duplicate username or email
    4. Hashes the password
    5. Creates user with initial balance of 100000
    
    Args:
        uid (str): Unique user identifier
        uname (str): Username (must be unique)
        password (str): Plain text password (will be hashed)
        email (str): Email address (must be unique)
        phone (str): Phone number
        
    Returns:
        dict: Result dictionary with:
            - success (bool): True if registration successful
            - message (str): Success or error message
            - error_code (str, optional): Error code if failed
            
    Requirements: 1.1, 1.2, 1.3, 1.4, 1.6, 6.1
    """
    # Validate all required fields are provided
    if not uid or not uname or not password or not email or not phone:
        logger.warning("Registration failed: missing required fields")
        return {
            'success': False,
            'message': 'All fields are required: uid, uname, password, email, phone',
            'error_code': 'VALIDATION_ERROR'
        }
    
    # Validate field formats
    try:
        if not validate_uid(uid):
            return {
                'success': False,
                'message': 'Invalid UID: must be non-empty string, max 50 characters',
                'error_code': 'VALIDATION_ERROR'
            }
        
        if not validate_username(uname):
            return {
                'success': False,
                'message': 'Invalid username: must be alphanumeric with underscores, 1-50 characters',
                'error_code': 'VALIDATION_ERROR'
            }
        
        if not validate_password(password):
            return {
                'success': False,
                'message': 'Invalid password: must be at least 6 characters',
                'error_code': 'VALIDATION_ERROR'
            }
        
        if not validate_email(email):
            return {
                'success': False,
                'message': 'Invalid email format',
                'error_code': 'VALIDATION_ERROR'
            }
        
        if not validate_phone(phone):
            return {
                'success': False,
                'message': 'Invalid phone format: must be 10-20 characters',
                'error_code': 'VALIDATION_ERROR'
            }
        
        # Create user with initial balance of 1000002
        # The create_user function handles duplicate checking and password hashing
        result = create_user(
            uid=uid,
            username=uname,
            password=password,
            email=email,
            phone=phone,
            balance=1000002.00
        )
        
        if result['success']:
            logger.info(f"User registered successfully: {uname}")
            return {
                'success': True,
                'message': 'Registration successful'
            }
        else:
            # Duplicate user case
            logger.warning(f"Registration failed for {uname}: {result['message']}")
            return {
                'success': False,
                'message': result['message'],
                'error_code': 'DUPLICATE_USER'
            }
            
    except ValueError as e:
        logger.error(f"Validation error during registration: {e}")
        return {
            'success': False,
            'message': str(e),
            'error_code': 'VALIDATION_ERROR'
        }
    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}")
        return {
            'success': False,
            'message': 'Internal server error during registration',
            'error_code': 'INTERNAL_ERROR'
        }


def login(username, password):
    """
    Authenticate user and generate JWT token.
    
    This function performs the complete login flow:
    1. Validates credentials against database
    2. Generates JWT token with username as subject and role as claim
    3. Stores token in CJWT table with expiry
    
    Args:
        username (str): Username for authentication
        password (str): Plain text password
        
    Returns:
        dict: Result dictionary with:
            - success (bool): True if login successful
            - message (str): Success or error message
            - token (str, optional): JWT token if successful
            - uid (str, optional): User ID if successful
            - error_code (str, optional): Error code if failed
            
    Requirements: 2.1, 2.2, 2.3, 2.4, 2.8, 5.1, 5.2, 6.2
    """
    # Validate inputs
    if not username or not password:
        logger.warning("Login failed: missing credentials")
        return {
            'success': False,
            'message': 'Username and password are required',
            'error_code': 'VALIDATION_ERROR'
        }
    
    try:
        # Fetch user record by username
        user = get_user_by_username(username)
        
        if not user:
            logger.warning(f"Login failed: user not found - {username}")
            return {
                'success': False,
                'message': 'Invalid credentials',
                'error_code': 'INVALID_CREDENTIALS'
            }
        
        # Verify password hash
        if not verify_password(password, user['password']):
            logger.warning(f"Login failed: invalid password for user - {username}")
            return {
                'success': False,
                'message': 'Invalid credentials',
                'error_code': 'INVALID_CREDENTIALS'
            }
        
        # Generate JWT token with username as subject and role as claim
        # All users get "customer" role as per requirements
        token = generate_token(username=username, role='customer')
        
        # Calculate expiry time (1 hour from now as per JWT service configuration)
        from jwt_service import JWT_EXPIRY_HOURS
        expiry = datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
        
        # Store token in CJWT table
        store_result = store_token(
            token=token,
            uid=user['uid'],
            expiry=expiry
        )
        
        if not store_result['success']:
            logger.error(f"Failed to store token for user: {username}")
            return {
                'success': False,
                'message': 'Failed to create session',
                'error_code': 'INTERNAL_ERROR'
            }
        
        logger.info(f"User logged in successfully: {username}")
        return {
            'success': True,
            'message': 'Login successful',
            'token': token,
            'uid': user['uid']
        }
        
    except ValueError as e:
        logger.error(f"Validation error during login: {e}")
        return {
            'success': False,
            'message': str(e),
            'error_code': 'VALIDATION_ERROR'
        }
    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        return {
            'success': False,
            'message': 'Internal server error during login',
            'error_code': 'INTERNAL_ERROR'
        }


def verify_token_from_request(token):
    """
    Extract and verify JWT token from request.
    
    This function validates the token signature, checks expiration,
    and extracts the username from the token payload.
    
    Args:
        token (str): JWT token from request (cookie or header)
        
    Returns:
        dict: Result dictionary with:
            - valid (bool): True if token is valid
            - username (str, optional): Username from token if valid
            - message (str): Success or error message
            - error_code (str, optional): Error code if invalid
            
    Requirements: 2.2, 2.3, 3.3, 3.9, 5.3, 5.4
    """
    # Check if token is provided
    if not token:
        logger.warning("Token verification failed: no token provided")
        return {
            'valid': False,
            'message': 'No token provided',
            'error_code': 'TOKEN_MISSING'
        }
    
    try:
        # Validate token signature and expiration
        if not validate_token(token):
            logger.warning("Token verification failed: invalid or expired token")
            return {
                'valid': False,
                'message': 'Invalid or expired token',
                'error_code': 'TOKEN_INVALID'
            }
        
        # Decode token to extract payload
        payload = decode_token(token)
        
        if not payload:
            logger.warning("Token verification failed: unable to decode token")
            return {
                'valid': False,
                'message': 'Invalid token format',
                'error_code': 'TOKEN_INVALID'
            }
        
        # Extract username from subject claim
        username = payload.get('sub')
        
        if not username:
            logger.warning("Token verification failed: no username in token")
            return {
                'valid': False,
                'message': 'Invalid token: missing username',
                'error_code': 'TOKEN_INVALID'
            }
        
        logger.info(f"Token verified successfully for user: {username}")
        return {
            'valid': True,
            'username': username,
            'message': 'Token is valid'
        }
        
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {e}")
        return {
            'valid': False,
            'message': 'Error verifying token',
            'error_code': 'INTERNAL_ERROR'
        }
