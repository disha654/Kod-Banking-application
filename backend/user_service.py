"""
User service module for kodbank1 application.

This module provides user management functionality including:
- User creation with password hashing
- User retrieval and validation
- Balance management
- Password verification

Requirements: 1.1, 1.4, 6.1, 6.2
"""

import re
import logging
import bcrypt
from mysql.connector import Error, IntegrityError
from db import execute_query

# Configure logging
logger = logging.getLogger(__name__)

# Bcrypt cost factor (work factor)
BCRYPT_COST_FACTOR = 10


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """
    Validate phone number format.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if phone format is valid, False otherwise
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # Allow digits, spaces, hyphens, parentheses, and plus sign
    # Length between 10 and 20 characters
    pattern = r'^[\d\s\-\(\)\+]{10,20}$'
    return re.match(pattern, phone) is not None


def validate_username(username):
    """
    Validate username format.
    
    Args:
        username (str): Username to validate
        
    Returns:
        bool: True if username format is valid, False otherwise
    """
    if not username or not isinstance(username, str):
        return False
    
    # Alphanumeric with underscores, 1-50 characters
    if len(username) > 50 or len(username) < 1:
        return False
    
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None


def validate_uid(uid):
    """
    Validate user ID format.
    
    Args:
        uid (str): User ID to validate
        
    Returns:
        bool: True if UID format is valid, False otherwise
    """
    if not uid or not isinstance(uid, str):
        return False
    
    # Non-empty string, max 50 characters
    return 0 < len(uid) <= 50


def validate_password(password):
    """
    Validate password format.
    
    Args:
        password (str): Password to validate
        
    Returns:
        bool: True if password format is valid, False otherwise
    """
    if not password or not isinstance(password, str):
        return False
    
    # Minimum 6 characters
    return len(password) >= 6


def hash_password(password):
    """
    Hash a password using bcrypt with cost factor 10.
    
    Args:
        password (str): Plain text password to hash
        
    Returns:
        str: Bcrypt hashed password
        
    Raises:
        ValueError: If password is invalid
    """
    if not validate_password(password):
        raise ValueError("Password must be at least 8 characters")
    
    # Generate salt and hash password
    salt = bcrypt.gensalt(rounds=BCRYPT_COST_FACTOR)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Return as string for database storage
    return hashed.decode('utf-8')


def verify_password(plain_password, hashed_password):
    """
    Verify a password against its bcrypt hash.
    
    Args:
        plain_password (str): Plain text password to verify
        hashed_password (str): Bcrypt hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        return False


def user_exists(username=None, email=None):
    """
    Check if a user exists by username or email.
    
    Args:
        username (str, optional): Username to check
        email (str, optional): Email to check
        
    Returns:
        bool: True if user exists, False otherwise
        
    Raises:
        ValueError: If neither username nor email is provided
    """
    if not username and not email:
        raise ValueError("Either username or email must be provided")
    
    try:
        if username and email:
            query = "SELECT COUNT(*) as count FROM kodusers WHERE username = %s OR email = %s"
            params = (username, email)
        elif username:
            query = "SELECT COUNT(*) as count FROM kodusers WHERE username = %s"
            params = (username,)
        else:
            query = "SELECT COUNT(*) as count FROM kodusers WHERE email = %s"
            params = (email,)
        
        results = execute_query(query, params, fetch=True)
        return results[0]['count'] > 0
        
    except Error as e:
        logger.error(f"Error checking user existence: {e}")
        raise


def create_user(uid, username, password, email, phone, balance=1000002.00):
    """
    Create a new user with hashed password and initial balance.
    
    Args:
        uid (str): Unique user identifier
        username (str): Username (must be unique)
        password (str): Plain text password (will be hashed)
        email (str): Email address (must be unique)
        phone (str): Phone number
        balance (float, optional): Initial balance (default: 100000.00)
        
    Returns:
        dict: Result dictionary with 'success' (bool) and 'message' (str)
        
    Raises:
        ValueError: If any input validation fails
    """
    # Validate all inputs
    if not validate_uid(uid):
        raise ValueError("Invalid UID: must be non-empty string, max 50 characters")
    
    if not validate_username(username):
        raise ValueError("Invalid username: must be alphanumeric with underscores, 1-50 characters")
    
    if not validate_password(password):
        raise ValueError("Invalid password: must be at least 8 characters")
    
    if not validate_email(email):
        raise ValueError("Invalid email format")
    
    if not validate_phone(phone):
        raise ValueError("Invalid phone format: must be 10-20 characters")
    
    try:
        # Check if user already exists
        if user_exists(username=username, email=email):
            return {
                'success': False,
                'message': 'Username or email already exists'
            }
        
        # Hash the password
        hashed_password = hash_password(password)
        
        # Insert user into database
        query = """
            INSERT INTO kodusers (uid, username, email, password, balance, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (uid, username, email, hashed_password, balance, phone)
        
        execute_query(query, params, fetch=False)
        
        logger.info(f"User created successfully: {username}")
        return {
            'success': True,
            'message': 'User created successfully'
        }
        
    except IntegrityError as e:
        logger.error(f"Integrity error creating user: {e}")
        return {
            'success': False,
            'message': 'Username or email already exists'
        }
    except Error as e:
        logger.error(f"Database error creating user: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating user: {e}")
        raise


def get_user_by_username(username):
    """
    Retrieve a user record by username.
    
    Args:
        username (str): Username to search for
        
    Returns:
        dict or None: User record dictionary if found, None otherwise
        
    Raises:
        ValueError: If username is invalid
    """
    if not validate_username(username):
        raise ValueError("Invalid username format")
    
    try:
        query = """
            SELECT uid, username, email, password, balance, phone, created_at
            FROM kodusers
            WHERE username = %s
        """
        params = (username,)
        
        results = execute_query(query, params, fetch=True)
        
        if results:
            return results[0]
        return None
        
    except Error as e:
        logger.error(f"Error retrieving user by username: {e}")
        raise


def get_balance(username):
    """
    Get the account balance for a user.
    
    Args:
        username (str): Username to get balance for
        
    Returns:
        float or None: Account balance if user found, None otherwise
        
    Raises:
        ValueError: If username is invalid
    """
    if not validate_username(username):
        raise ValueError("Invalid username format")
    
    try:
        query = "SELECT balance FROM kodusers WHERE username = %s"
        params = (username,)
        
        results = execute_query(query, params, fetch=True)
        
        if results:
            return float(results[0]['balance'])
        return None
        
    except Error as e:
        logger.error(f"Error retrieving balance: {e}")
        raise


def transfer_money(sender_username, receiver_username, amount):
    """
    Transfer money from sender to receiver.
    
    This function performs a money transfer between two users:
    1. Validates sender and receiver exist
    2. Checks sender has sufficient balance
    3. Deducts amount from sender
    4. Adds amount to receiver
    
    Args:
        sender_username (str): Username of the sender
        receiver_username (str): Username of the receiver
        amount (float): Amount to transfer (must be positive)
        
    Returns:
        dict: Result dictionary with:
            - success (bool): True if transfer successful
            - message (str): Success or error message
            - error_code (str, optional): Error code if failed
            - sender_balance (float, optional): New sender balance if successful
            - receiver_balance (float, optional): New receiver balance if successful
    """
    # Validate inputs
    if not validate_username(sender_username):
        return {
            'success': False,
            'message': 'Invalid sender username format',
            'error_code': 'VALIDATION_ERROR'
        }
    
    if not validate_username(receiver_username):
        return {
            'success': False,
            'message': 'Invalid receiver username format',
            'error_code': 'VALIDATION_ERROR'
        }
    
    # Validate amount
    try:
        amount = float(amount)
        if amount <= 0:
            return {
                'success': False,
                'message': 'Transfer amount must be greater than zero',
                'error_code': 'INVALID_AMOUNT'
            }
    except (ValueError, TypeError):
        return {
            'success': False,
            'message': 'Invalid amount format',
            'error_code': 'VALIDATION_ERROR'
        }
    
    # Check if sender and receiver are the same
    if sender_username == receiver_username:
        return {
            'success': False,
            'message': 'Cannot transfer money to yourself',
            'error_code': 'INVALID_TRANSFER'
        }
    
    try:
        # Get sender details
        sender = get_user_by_username(sender_username)
        if not sender:
            return {
                'success': False,
                'message': 'Sender account not found',
                'error_code': 'SENDER_NOT_FOUND'
            }
        
        # Get receiver details
        receiver = get_user_by_username(receiver_username)
        if not receiver:
            return {
                'success': False,
                'message': 'Receiver account not found',
                'error_code': 'RECEIVER_NOT_FOUND'
            }
        
        # Check if sender has sufficient balance
        sender_balance = float(sender['balance'])
        if sender_balance < amount:
            return {
                'success': False,
                'message': f'Insufficient balance. Available: {sender_balance}',
                'error_code': 'INSUFFICIENT_BALANCE'
            }
        
        # Calculate new balances
        new_sender_balance = sender_balance - amount
        new_receiver_balance = float(receiver['balance']) + amount
        
        # Update sender balance
        update_sender_query = """
            UPDATE kodusers 
            SET balance = %s 
            WHERE username = %s
        """
        execute_query(update_sender_query, (new_sender_balance, sender_username), fetch=False)
        
        # Update receiver balance
        update_receiver_query = """
            UPDATE kodusers 
            SET balance = %s 
            WHERE username = %s
        """
        execute_query(update_receiver_query, (new_receiver_balance, receiver_username), fetch=False)
        
        # Record transaction in transactions table
        insert_transaction_query = """
            INSERT INTO transactions (sender_username, receiver_username, amount, transaction_type, status)
            VALUES (%s, %s, %s, 'transfer', 'completed')
        """
        execute_query(insert_transaction_query, (sender_username, receiver_username, amount), fetch=False)
        
        logger.info(f"Transfer successful: {sender_username} -> {receiver_username}, Amount: {amount}")
        
        return {
            'success': True,
            'message': f'Successfully transferred {amount} to {receiver_username}',
            'sender_balance': new_sender_balance,
            'receiver_balance': new_receiver_balance
        }
        
    except Error as e:
        logger.error(f"Database error during transfer: {e}")
        return {
            'success': False,
            'message': 'Transfer failed due to database error',
            'error_code': 'DATABASE_ERROR'
        }
    except Exception as e:
        logger.error(f"Unexpected error during transfer: {e}")
        return {
            'success': False,
            'message': 'Transfer failed due to unexpected error',
            'error_code': 'INTERNAL_ERROR'
        }


def get_transaction_history(username, limit=10):
    """
    Get transaction history for a user.
    
    Returns both sent and received transactions, ordered by most recent first.
    
    Args:
        username (str): Username to get transaction history for
        limit (int, optional): Maximum number of transactions to return (default: 10)
        
    Returns:
        list: List of transaction dictionaries with:
            - id (int): Transaction ID
            - sender_username (str): Sender username
            - receiver_username (str): Receiver username
            - amount (float): Transaction amount
            - transaction_type (str): Type of transaction
            - status (str): Transaction status
            - created_at (datetime): Transaction timestamp
            - direction (str): 'sent' or 'received' from user's perspective
    """
    if not validate_username(username):
        raise ValueError("Invalid username format")
    
    try:
        query = """
            SELECT 
                id,
                sender_username,
                receiver_username,
                amount,
                transaction_type,
                status,
                created_at,
                CASE 
                    WHEN sender_username = %s THEN 'sent'
                    ELSE 'received'
                END as direction
            FROM transactions
            WHERE sender_username = %s OR receiver_username = %s
            ORDER BY created_at DESC
            LIMIT %s
        """
        params = (username, username, username, limit)
        
        results = execute_query(query, params, fetch=True)
        
        # Convert Decimal to float for JSON serialization
        for transaction in results:
            transaction['amount'] = float(transaction['amount'])
        
        return results
        
    except Error as e:
        logger.error(f"Error retrieving transaction history: {e}")
        raise
