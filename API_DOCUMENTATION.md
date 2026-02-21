# kodbank1 API Documentation

## Overview

The kodbank1 API provides secure banking operations including user registration, authentication, and balance inquiry. All endpoints use JSON for request and response bodies, and authentication is handled via JWT tokens stored in HTTP-only cookies.

**Base URL:** `http://localhost:5000/api`

**Authentication:** JWT token in HTTP-only cookie (automatically sent by browser)

**Content-Type:** `application/json`

---

## Authentication Flow

### Overview

kodbank1 uses JWT (JSON Web Token) based authentication with the following flow:

```
1. User Registration
   └─> POST /api/register
       └─> User account created with initial balance

2. User Login
   └─> POST /api/login
       └─> JWT token generated and stored in:
           ├─> HTTP-only cookie (client-side)
           └─> CJWT table (server-side)

3. Authenticated Requests
   └─> GET /api/balance (with JWT cookie)
       └─> Token validated:
           ├─> Signature verification
           ├─> Expiration check
           └─> Database lookup
       └─> Request processed if valid
```

### Token Structure

JWT tokens contain the following claims:

```json
{
  "sub": "username",      // Subject: username of authenticated user
  "role": "customer",     // User role (always "customer" for registered users)
  "iat": 1234567890,      // Issued At: Unix timestamp
  "exp": 1234571490       // Expiration: Unix timestamp (1 hour after iat)
}
```

### Token Storage

- **Client-side:** HTTP-only, Secure, SameSite=Strict cookie
- **Server-side:** CJWT table with expiry timestamp
- **Expiration:** 1 hour (configurable via JWT_EXPIRY_HOURS)

### Token Validation

All authenticated endpoints validate tokens by:
1. Extracting token from cookie
2. Verifying signature using JWT_SECRET_KEY
3. Checking expiration timestamp
4. Confirming token exists in CJWT table

---

## Endpoints

### 1. Register User

Create a new user account with an initial balance of 1,000,002.

**Endpoint:** `POST /api/register`

**Authentication:** Not required

**Request Body:**

```json
{
  "uid": "string",        // Unique user identifier (max 50 chars)
  "uname": "string",      // Username (max 50 chars, alphanumeric + underscore)
  "password": "string",   // Password (min 8 chars, will be hashed)
  "email": "string",      // Email address (valid email format, max 100 chars)
  "phone": "string"       // Phone number (max 20 chars)
}
```

**Example Request:**

```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "user123",
    "uname": "johndoe",
    "password": "SecurePass123!",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123"
  }'
```

**Success Response (200 OK):**

```json
{
  "status": "success",
  "message": "Registration successful"
}
```

**Error Responses:**

**400 Bad Request - Missing Fields:**
```json
{
  "status": "error",
  "message": "Missing required fields: uid, uname, password, email, phone",
  "code": "VALIDATION_ERROR",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**400 Bad Request - Invalid Email:**
```json
{
  "status": "error",
  "message": "Invalid email format",
  "code": "VALIDATION_ERROR",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**409 Conflict - Duplicate Username:**
```json
{
  "status": "error",
  "message": "Username already exists",
  "code": "DUPLICATE_USER",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**409 Conflict - Duplicate Email:**
```json
{
  "status": "error",
  "message": "Email already exists",
  "code": "DUPLICATE_USER",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**500 Internal Server Error:**
```json
{
  "status": "error",
  "message": "Internal server error",
  "code": "INTERNAL_ERROR",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Requirements Validated:**
- 1.1: All required fields validated
- 1.2: Role "customer" assigned automatically
- 1.3: Initial balance set to 1,000,002
- 1.4: User information stored in kodusers table
- 1.6: Duplicate username/email rejected

---

### 2. Login

Authenticate user credentials and establish a session with JWT token.

**Endpoint:** `POST /api/login`

**Authentication:** Not required

**Request Body:**

```json
{
  "username": "string",   // Username (required)
  "password": "string"    // Password (required)
}
```

**Example Request:**

```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

**Success Response (200 OK):**

```json
{
  "status": "success",
  "message": "Login successful"
}
```

**Response Headers:**
```
Set-Cookie: jwt=<token>; HttpOnly; Secure; SameSite=Strict; Max-Age=3600; Path=/
```

**Cookie Attributes:**
- `HttpOnly`: Prevents JavaScript access (XSS protection)
- `Secure`: Only transmitted over HTTPS
- `SameSite=Strict`: CSRF protection
- `Max-Age=3600`: Expires in 1 hour (3600 seconds)
- `Path=/`: Available for all paths

**Error Responses:**

**400 Bad Request - Missing Fields:**
```json
{
  "status": "error",
  "message": "Username and password are required",
  "code": "VALIDATION_ERROR",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**400 Bad Request - No JSON Body:**
```json
{
  "status": "error",
  "message": "Request must contain JSON data",
  "code": "VALIDATION_ERROR",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**401 Unauthorized - Invalid Credentials:**
```json
{
  "status": "error",
  "message": "Invalid credentials",
  "code": "INVALID_CREDENTIALS",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**500 Internal Server Error:**
```json
{
  "status": "error",
  "message": "Internal server error",
  "code": "INTERNAL_ERROR",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Requirements Validated:**
- 2.1: Credentials validated against kodusers table
- 2.2: JWT token generated with username and role
- 2.3: Standard signature key generation algorithm used
- 2.4: Token stored in CJWT table
- 2.5: Token added as cookie to response
- 2.6: Success status sent on authentication
- 2.8: Invalid credentials rejected with error

---

### 3. Get Balance

Retrieve the authenticated user's account balance.

**Endpoint:** `GET /api/balance`

**Authentication:** Required (JWT token in cookie)

**Request Headers:**
```
Cookie: jwt=<token>
```

**Request Body:** None

**Example Request:**

```bash
curl -X GET http://localhost:5000/api/balance \
  -H "Cookie: jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Success Response (200 OK):**

```json
{
  "status": "success",
  "balance": 1000002.00
}
```

**Error Responses:**

**401 Unauthorized - Missing Token:**
```json
{
  "status": "error",
  "message": "No token provided",
  "code": "TOKEN_MISSING",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**401 Unauthorized - Expired Token:**
```json
{
  "status": "error",
  "message": "Token expired",
  "code": "TOKEN_EXPIRED",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**401 Unauthorized - Invalid Token:**
```json
{
  "status": "error",
  "message": "Invalid token",
  "code": "TOKEN_INVALID",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**401 Unauthorized - User Not Found:**
```json
{
  "status": "error",
  "message": "User not found",
  "code": "UNAUTHORIZED",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**500 Internal Server Error:**
```json
{
  "status": "error",
  "message": "Internal server error",
  "code": "INTERNAL_ERROR",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

**Requirements Validated:**
- 3.2: Request sent with JWT token
- 3.3: Backend verifies and validates JWT token
- 3.4: Token is valid
- 3.5: Username extracted from token
- 3.6: Balance fetched from kodusers table
- 3.9: Invalid/expired tokens rejected with authentication error

---

## Error Codes Reference

### Complete Error Code List

| Error Code | HTTP Status | Description | Possible Causes |
|------------|-------------|-------------|-----------------|
| `VALIDATION_ERROR` | 400 | Input validation failed | Missing fields, invalid formats, empty values |
| `DUPLICATE_USER` | 409 | Username or email already exists | Registration with existing username/email |
| `INVALID_CREDENTIALS` | 401 | Username or password incorrect | Wrong username or password during login |
| `TOKEN_MISSING` | 401 | No JWT token provided | Request without authentication cookie |
| `TOKEN_EXPIRED` | 401 | JWT token has expired | Token older than 1 hour |
| `TOKEN_INVALID` | 401 | JWT token signature invalid or malformed | Tampered token, wrong secret key, corrupted token |
| `UNAUTHORIZED` | 401 | Authentication required | Valid token but user doesn't exist |
| `DATABASE_ERROR` | 500 | Database operation failed | Connection issues, query errors |
| `INTERNAL_ERROR` | 500 | Unexpected server error | Unhandled exceptions, system errors |

### Error Response Format

All error responses follow this consistent structure:

```json
{
  "status": "error",
  "message": "Human-readable error description",
  "code": "ERROR_CODE",
  "timestamp": "ISO 8601 timestamp"
}
```

**Fields:**
- `status`: Always "error" for error responses
- `message`: Human-readable description of the error
- `code`: Machine-readable error code (see table above)
- `timestamp`: UTC timestamp in ISO 8601 format

---

## Security Considerations

### Password Security

- Passwords are hashed using bcrypt with cost factor 10
- Plaintext passwords are never stored in the database
- Password hashes are never returned in API responses

### Token Security

- JWT tokens use HS256 (HMAC with SHA-256) algorithm
- Secret key is stored securely in environment variables
- Tokens expire after 1 hour (configurable)
- Tokens are stored in HTTP-only cookies to prevent XSS attacks
- Secure flag ensures tokens only transmitted over HTTPS
- SameSite=Strict prevents CSRF attacks

### Database Security

- All connections use SSL/TLS encryption
- Connection strings stored in environment variables
- Prepared statements prevent SQL injection
- Foreign key constraints maintain data integrity

### API Security

- CORS configured to allow specific origins only
- Security headers prevent common attacks:
  - Content-Security-Policy: XSS protection
  - X-Frame-Options: Clickjacking protection
  - X-Content-Type-Options: MIME sniffing protection
  - Strict-Transport-Security: HTTPS enforcement

### Data Protection

- Sensitive data never exposed in error messages
- Database credentials never returned in responses
- JWT signing keys never exposed to clients
- User passwords never logged or returned

---

## Rate Limiting

**Current Status:** Not implemented

**Recommendation:** Implement rate limiting for production:
- Registration: 5 requests per hour per IP
- Login: 10 requests per 15 minutes per IP
- Balance: 100 requests per hour per user

---

## Testing the API

### Using cURL

**Register a new user:**
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "uid": "test123",
    "uname": "testuser",
    "password": "TestPass123!",
    "email": "test@example.com",
    "phone": "+1-555-9999"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'
```

**Get balance:**
```bash
curl -X GET http://localhost:5000/api/balance \
  -b cookies.txt
```

### Using JavaScript Fetch API

**Register:**
```javascript
fetch('http://localhost:5000/api/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    uid: 'test123',
    uname: 'testuser',
    password: 'TestPass123!',
    email: 'test@example.com',
    phone: '+1-555-9999'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

**Login:**
```javascript
fetch('http://localhost:5000/api/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  credentials: 'include',  // Important: sends cookies
  body: JSON.stringify({
    username: 'testuser',
    password: 'TestPass123!'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

**Get Balance:**
```javascript
fetch('http://localhost:5000/api/balance', {
  method: 'GET',
  credentials: 'include'  // Important: sends cookies
})
.then(response => response.json())
.then(data => console.log(data));
```

### Using Postman

1. **Register:**
   - Method: POST
   - URL: `http://localhost:5000/api/register`
   - Headers: `Content-Type: application/json`
   - Body (raw JSON): See request body format above

2. **Login:**
   - Method: POST
   - URL: `http://localhost:5000/api/login`
   - Headers: `Content-Type: application/json`
   - Body (raw JSON): See request body format above
   - Note: Cookie will be automatically saved

3. **Get Balance:**
   - Method: GET
   - URL: `http://localhost:5000/api/balance`
   - Note: Cookie will be automatically sent

---

## Versioning

**Current Version:** 1.0

**API Stability:** Stable

**Breaking Changes:** None planned

**Future Enhancements:**
- Account transfers
- Transaction history
- Password reset
- Multi-factor authentication
- Account statements

---

## Support

For API issues or questions:
- Check error codes and messages
- Review authentication flow
- Verify request format matches examples
- Check server logs for detailed error information

---

## Changelog

### Version 1.0 (Initial Release)
- User registration endpoint
- User login with JWT authentication
- Balance inquiry endpoint
- Comprehensive error handling
- Security headers and CORS configuration
