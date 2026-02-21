"""
Flask application for kodbank1 banking system.

This module provides the main Flask application with API endpoints for:
- User registration
- User login
- Balance inquiry
- Money transfer

Requirements: 1.1, 1.5, 1.6, 2.1, 2.5, 2.6, 2.8, 3.2, 3.3, 3.4, 3.5, 3.6, 3.9
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
from auth_service import register_user, login, verify_token_from_request
from user_service import get_balance, transfer_money, get_transaction_history
from db import initialize_connection_pool, test_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)

# Configuration
app.config['JSON_SORT_KEYS'] = False

# Configure CORS to allow frontend origin with credentials support
# This allows the frontend to send cookies (JWT tokens) with requests
# Task 12.1: Configure CORS for Flask app
# Allow all origins in production (Vercel deployment) or specific origins in development
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*')
if allowed_origins == '*':
    CORS(app, 
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    )
else:
    origins_list = [origin.strip() for origin in allowed_origins.split(',')]
    CORS(app, 
         origins=origins_list,
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    )

# Initialize database connection pool
# This can be skipped in testing mode by setting SKIP_DB_INIT=1
if not os.getenv('SKIP_DB_INIT'):
    try:
        initialize_connection_pool()
        logger.info("Database connection pool initialized")
        
        # Verify database connection on startup
        if test_connection():
            logger.info("✓ Database connection verified successfully")
        else:
            logger.error("✗ Database connection verification failed")
            raise Exception("Database connection test failed")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
else:
    logger.warning("Database initialization skipped (SKIP_DB_INIT=1)")


# Task 12.2: Add security headers middleware
@app.after_request
def add_security_headers(response):
    """
    Add helmet-like security headers to all responses.
    
    Security headers added:
    - Content-Security-Policy: Restricts resource loading to prevent XSS
    - X-Content-Type-Options: Prevents MIME type sniffing
    - X-Frame-Options: Prevents clickjacking attacks
    - X-XSS-Protection: Enables browser XSS protection
    - Strict-Transport-Security: Enforces HTTPS connections
    - Referrer-Policy: Controls referrer information
    
    Task 12.2: Add security headers
    """
    # Content Security Policy - restricts resource loading
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none'"
    )
    
    # Prevent MIME type sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Prevent clickjacking by disallowing iframe embedding
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Enable browser XSS protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Enforce HTTPS connections (only in production)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Control referrer information
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Prevent browsers from performing DNS prefetching
    response.headers['X-DNS-Prefetch-Control'] = 'off'
    
    # Disable browser features that could be exploited
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    return response


@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user account."""
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("Registration request missing JSON body")
            return jsonify({
                'status': 'error',
                'message': 'Request must contain JSON data',
                'code': 'VALIDATION_ERROR',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        uid = data.get('uid')
        uname = data.get('uname')
        password = data.get('password')
        email = data.get('email')
        phone = data.get('phone')
        
        result = register_user(
            uid=uid,
            uname=uname,
            password=password,
            email=email,
            phone=phone
        )
        
        if result['success']:
            logger.info(f"Registration successful for user: {uname}")
            return jsonify({
                'status': 'success',
                'message': result['message']
            }), 200
        else:
            status_code = 409 if result.get('error_code') == 'DUPLICATE_USER' else 400
            
            logger.warning(f"Registration failed: {result['message']}")
            return jsonify({
                'status': 'error',
                'message': result['message'],
                'code': result.get('error_code', 'ERROR'),
                'timestamp': datetime.utcnow().isoformat()
            }), status_code
            
    except Exception as e:
        logger.error(f"Unexpected error in register endpoint: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'timestamp': datetime.utcnow().isoformat()
        }), 500


@app.route('/api/login', methods=['POST'])
def login_endpoint():
    """Authenticate user and establish session."""
    try:
        data = request.get_json()
        
        if not data:
            logger.warning("Login request missing JSON body")
            return jsonify({
                'status': 'error',
                'message': 'Request must contain JSON data',
                'code': 'VALIDATION_ERROR',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            logger.warning("Login request missing username or password")
            return jsonify({
                'status': 'error',
                'message': 'Username and password are required',
                'code': 'VALIDATION_ERROR',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        result = login(username=username, password=password)
        
        if result['success']:
            logger.info(f"Login successful for user: {username}")
            
            response = make_response(jsonify({
                'status': 'success',
                'message': result['message']
            }), 200)
            
            response.set_cookie(
                'jwt',
                value=result['token'],
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=3600
            )
            
            return response
        else:
            status_code = 401 if result.get('error_code') == 'INVALID_CREDENTIALS' else 400
            
            logger.warning(f"Login failed for user {username}: {result['message']}")
            return jsonify({
                'status': 'error',
                'message': result['message'],
                'code': result.get('error_code', 'ERROR'),
                'timestamp': datetime.utcnow().isoformat()
            }), status_code
            
    except Exception as e:
        logger.error(f"Unexpected error in login endpoint: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'timestamp': datetime.utcnow().isoformat()
        }), 500


@app.route('/api/balance', methods=['GET'])
def balance():
    """Retrieve authenticated user's account balance."""
    try:
        token = request.cookies.get('jwt')
        
        verification_result = verify_token_from_request(token)
        
        if not verification_result['valid']:
            error_code = verification_result.get('error_code', 'UNAUTHORIZED')
            logger.warning(f"Balance request failed: {verification_result['message']}")
            return jsonify({
                'status': 'error',
                'message': verification_result['message'],
                'code': error_code,
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        username = verification_result['username']
        
        balance = get_balance(username)
        
        if balance is None:
            logger.error(f"Balance not found for user: {username}")
            return jsonify({
                'status': 'error',
                'message': 'User not found',
                'code': 'UNAUTHORIZED',
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        logger.info(f"Balance retrieved successfully for user: {username}")
        return jsonify({
            'status': 'success',
            'balance': balance
        }), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in balance endpoint: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'timestamp': datetime.utcnow().isoformat()
        }), 500


@app.route('/api/transfer', methods=['POST'])
def transfer():
    """Transfer money from authenticated user to another user."""
    try:
        token = request.cookies.get('jwt')
        
        verification_result = verify_token_from_request(token)
        
        if not verification_result['valid']:
            error_code = verification_result.get('error_code', 'UNAUTHORIZED')
            logger.warning(f"Transfer request failed: {verification_result['message']}")
            return jsonify({
                'status': 'error',
                'message': verification_result['message'],
                'code': error_code,
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        sender_username = verification_result['username']
        
        data = request.get_json()
        
        if not data:
            logger.warning("Transfer request missing JSON body")
            return jsonify({
                'status': 'error',
                'message': 'Request must contain JSON data',
                'code': 'VALIDATION_ERROR',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        receiver_username = data.get('receiver_username')
        amount = data.get('amount')
        
        if not receiver_username or amount is None:
            logger.warning("Transfer request missing receiver_username or amount")
            return jsonify({
                'status': 'error',
                'message': 'Receiver username and amount are required',
                'code': 'VALIDATION_ERROR',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        result = transfer_money(
            sender_username=sender_username,
            receiver_username=receiver_username,
            amount=amount
        )
        
        if result['success']:
            logger.info(f"Transfer successful: {sender_username} -> {receiver_username}, Amount: {amount}")
            return jsonify({
                'status': 'success',
                'message': result['message'],
                'sender_balance': result['sender_balance'],
                'receiver_balance': result['receiver_balance']
            }), 200
        else:
            status_code = 400
            if result.get('error_code') in ['SENDER_NOT_FOUND', 'RECEIVER_NOT_FOUND']:
                status_code = 404
            elif result.get('error_code') == 'INSUFFICIENT_BALANCE':
                status_code = 400
            
            logger.warning(f"Transfer failed: {result['message']}")
            return jsonify({
                'status': 'error',
                'message': result['message'],
                'code': result.get('error_code', 'ERROR'),
                'timestamp': datetime.utcnow().isoformat()
            }), status_code
            
    except Exception as e:
        logger.error(f"Unexpected error in transfer endpoint: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'timestamp': datetime.utcnow().isoformat()
        }), 500


@app.route('/api/transactions', methods=['GET'])
def transactions():
    """Get transaction history for authenticated user."""
    try:
        token = request.cookies.get('jwt')
        
        verification_result = verify_token_from_request(token)
        
        if not verification_result['valid']:
            error_code = verification_result.get('error_code', 'UNAUTHORIZED')
            logger.warning(f"Transactions request failed: {verification_result['message']}")
            return jsonify({
                'status': 'error',
                'message': verification_result['message'],
                'code': error_code,
                'timestamp': datetime.utcnow().isoformat()
            }), 401
        
        username = verification_result['username']
        
        # Get limit from query parameter (default: 10)
        limit = request.args.get('limit', 10, type=int)
        
        # Fetch transaction history
        transaction_list = get_transaction_history(username, limit=limit)
        
        logger.info(f"Transaction history retrieved for user: {username}")
        return jsonify({
            'status': 'success',
            'transactions': transaction_list
        }), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in transactions endpoint: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'timestamp': datetime.utcnow().isoformat()
        }), 500


# Serve frontend files (only for local development)
# In Vercel, frontend files are served directly by Vercel's CDN
@app.route('/')
def index():
    """Serve the registration page as the default landing page."""
    try:
        return send_from_directory('../frontend', 'register.html')
    except:
        return jsonify({'message': 'Frontend files served by Vercel CDN'}), 200


@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend static files (HTML, CSS, JS)."""
    try:
        return send_from_directory('../frontend', path)
    except:
        return jsonify({'message': 'Frontend files served by Vercel CDN'}), 200


if __name__ == '__main__':
    logger.info("Starting kodbank1 Flask application")
    app.run(debug=True, host='0.0.0.0', port=5000)
