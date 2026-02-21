# Authentication Service Module

## Overview

The `auth_service.py` module provides complete authentication functionality for the kodbank1 banking application. It integrates the user service and JWT service to handle user registration, login, and token verification.

## Requirements Addressed

- **1.1**: Validates all required registration fields (uid, uname, password, email, phone)
- **1.6**: Checks for duplicate username or email during registration
- **2.1**: Validates user credentials against database
- **2.2**: Generates JWT tokens with username as subject and role as claim
- **2.4**: Stores JWT tokens in CJWT table with expiry
- **2.8**: Returns appropriate error messages for invalid credentials

## Functions

### `register_user(uid, uname, password, email, phone)`

Registers a new user with complete validation and duplicate checking.

**Parameters:**
- `uid` (str): Unique user identifier
- `uname` (str): Username (must be unique)
- `password` (str): Plain text password (will be hashed)
- `email` (str): Email address (must be unique)
- `phone` (str): Phone number

**Returns:**
```python
{
    'success': bool,           # True if registration successful
    'message': str,            # Success or error message
    'error_code': str          # Error code if failed (optional)
}
```

**Error Codes:**
- `VALIDATION_ERROR`: Invalid input format or missing fields
- `DUPLICATE_USER`: Username or email already exists
- `INTERNAL_ERROR`: Unexpected server error

**Example:**
```python
from auth_service import register_user

result = register_user(
    uid="user123",
    uname="johndoe",
    password="securepass123",
    email="john@example.com",
    phone="1234567890"
)

if result['success']:
    print("Registration successful!")
else:
    print(f"Error: {result['message']}")
```

**Validation Rules:**
- All fields are required
- UID: Non-empty string, max 50 characters
- Username: Alphanumeric with underscores, 1-50 characters
- Password: Minimum 8 characters
- Email: Valid email format
- Phone: 10-20 characters

**Process Flow:**
1. Validates all required fields are provided
2. Validates field formats
3. Checks for duplicate username or email
4. Hashes the password using bcrypt
5. Creates user with initial balance of 100000
6. Returns success or error response

---

### `login(username, password)`

Authenticates user and generates JWT token.

**Parameters:**
- `username` (str): Username for authentication
- `password` (str): Plain text password

**Returns:**
```python
{
    'success': bool,           # True if login successful
    'message': str,            # Success or error message
    'token': str,              # JWT token (if successful)
    'uid': str,                # User ID (if successful)
    'error_code': str          # Error code if failed (optional)
}
```

**Error Codes:**
- `VALIDATION_ERROR`: Missing username or password
- `INVALID_CREDENTIALS`: Username or password incorrect
- `INTERNAL_ERROR`: Unexpected server error

**Example:**
```python
from auth_service import login

result = login(
    username="johndoe",
    password="securepass123"
)

if result['success']:
    token = result['token']
    print(f"Login successful! Token: {token}")
else:
    print(f"Error: {result['message']}")
```

**Process Flow:**
1. Validates credentials are provided
2. Fetches user record by username
3. Verifies password hash matches
4. Generates JWT token with username as subject and "customer" as role
5. Stores token in CJWT table with 1-hour expiry
6. Returns token and user ID

**Security Notes:**
- Password is verified using bcrypt
- Error messages don't reveal whether username or password is incorrect
- JWT token expires after 1 hour (configurable via JWT_EXPIRY_HOURS)
- Token is stored in database for validation and revocation

---

### `verify_token_from_request(token)`

Extracts and verifies JWT token from request.

**Parameters:**
- `token` (str): JWT token from request (cookie or header)

**Returns:**
```python
{
    'valid': bool,             # True if token is valid
    'username': str,           # Username from token (if valid)
    'message': str,            # Success or error message
    'error_code': str          # Error code if invalid (optional)
}
```

**Error Codes:**
- `TOKEN_MISSING`: No token provided
- `TOKEN_INVALID`: Invalid signature, expired, or malformed token
- `INTERNAL_ERROR`: Unexpected server error

**Example:**
```python
from auth_service import verify_token_from_request

# Extract token from request cookie or header
token = request.cookies.get('jwt')

result = verify_token_from_request(token)

if result['valid']:
    username = result['username']
    print(f"Authenticated user: {username}")
else:
    print(f"Authentication failed: {result['message']}")
```

**Process Flow:**
1. Checks if token is provided
2. Validates token signature using JWT secret key
3. Checks token expiration
4. Decodes token payload
5. Extracts username from subject claim
6. Returns validation result with username

**Token Validation:**
- Verifies JWT signature using HS256 algorithm
- Checks token has not expired
- Validates token structure and required claims
- Extracts username from 'sub' (subject) claim

---

## Integration with Other Services

### User Service Integration

The auth_service uses the following functions from `user_service.py`:
- `create_user()`: Creates new user with hashed password
- `get_user_by_username()`: Retrieves user record for authentication
- `verify_password()`: Verifies password against bcrypt hash
- Validation functions: `validate_uid()`, `validate_username()`, etc.

### JWT Service Integration

The auth_service uses the following functions from `jwt_service.py`:
- `generate_token()`: Creates JWT with username and role claims
- `validate_token()`: Verifies token signature and expiration
- `decode_token()`: Extracts payload from token
- `store_token()`: Saves token to CJWT table

---

## Error Handling

All functions return structured error responses with:
- Clear error messages for users
- Error codes for programmatic handling
- Appropriate logging for debugging

**Common Error Scenarios:**

1. **Registration Errors:**
   - Missing or invalid fields → `VALIDATION_ERROR`
   - Duplicate username/email → `DUPLICATE_USER`
   - Database errors → `INTERNAL_ERROR`

2. **Login Errors:**
   - Missing credentials → `VALIDATION_ERROR`
   - Invalid username/password → `INVALID_CREDENTIALS`
   - Token generation/storage failure → `INTERNAL_ERROR`

3. **Token Verification Errors:**
   - No token provided → `TOKEN_MISSING`
   - Invalid/expired token → `TOKEN_INVALID`
   - Decoding errors → `INTERNAL_ERROR`

---

## Testing

### Unit Tests

Run the unit tests (no database required):
```bash
python backend/test_auth_service_unit.py
```

Tests cover:
- Module imports and function signatures
- Input validation logic
- Error code generation
- Requirements coverage

### Integration Tests

For full integration testing with database:
```bash
python backend/test_auth_service.py
```

Requires:
- Valid DATABASE_URL in .env file
- Database connection pool initialized
- kodusers and CJWT tables created

---

## Usage in Flask API

Example integration with Flask endpoints:

```python
from flask import Flask, request, jsonify, make_response
from auth_service import register_user, login, verify_token_from_request

app = Flask(__name__)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    result = register_user(
        uid=data.get('uid'),
        uname=data.get('uname'),
        password=data.get('password'),
        email=data.get('email'),
        phone=data.get('phone')
    )
    
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code

@app.route('/api/login', methods=['POST'])
def login_endpoint():
    data = request.json
    result = login(
        username=data.get('username'),
        password=data.get('password')
    )
    
    if result['success']:
        response = make_response(jsonify({
            'status': 'success',
            'message': result['message']
        }))
        # Set JWT token as HTTP-only cookie
        response.set_cookie(
            'jwt',
            result['token'],
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=3600
        )
        return response
    else:
        return jsonify(result), 401

@app.route('/api/balance', methods=['GET'])
def get_balance():
    token = request.cookies.get('jwt')
    result = verify_token_from_request(token)
    
    if not result['valid']:
        return jsonify(result), 401
    
    # Proceed with balance retrieval using result['username']
    # ...
```

---

## Security Considerations

1. **Password Security:**
   - Passwords are hashed using bcrypt with cost factor 10
   - Plain text passwords are never stored
   - Password verification uses constant-time comparison

2. **Token Security:**
   - JWT tokens use HS256 signature algorithm
   - Tokens expire after 1 hour
   - Tokens are stored in database for validation
   - Secret key must be kept secure (use environment variables)

3. **Error Messages:**
   - Generic error messages prevent information disclosure
   - Login errors don't reveal if username or password is wrong
   - Detailed errors are logged server-side only

4. **Input Validation:**
   - All inputs are validated before processing
   - SQL injection prevented by parameterized queries
   - XSS prevented by not storing/returning HTML

---

## Dependencies

- `user_service`: User management and password hashing
- `jwt_service`: JWT token generation and validation
- `bcrypt`: Password hashing
- `PyJWT`: JWT token handling
- `mysql-connector-python`: Database connectivity

---

## Configuration

Required environment variables (in `.env` file):

```env
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here-change-this-in-production
JWT_EXPIRY_HOURS=1

# Database Configuration
DATABASE_URL=mysql://user:pass@host:port/db?ssl-mode=REQUIRED
```

---

## Logging

The module uses Python's logging framework:

- **INFO**: Successful operations (registration, login, token verification)
- **WARNING**: Failed authentication attempts, validation errors
- **ERROR**: Database errors, unexpected exceptions

Configure logging in your application:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```
