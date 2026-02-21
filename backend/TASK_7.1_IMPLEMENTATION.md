# Task 7.1 Implementation: Flask Application and Register Endpoint

## Overview

This document describes the implementation of Task 7.1, which creates the Flask application and implements the POST /api/register endpoint.

## Files Created

1. **backend/app.py** - Main Flask application with register endpoint
2. **backend/test_app_register.py** - Unit tests for the register endpoint
3. **backend/verify_app.py** - Verification script for app structure

## Implementation Details

### Flask Application (app.py)

The Flask application includes:

1. **Application Initialization**
   - Flask app created with proper configuration
   - Database connection pool initialized on startup
   - Logging configured for debugging and monitoring

2. **POST /api/register Endpoint**
   - Route: `/api/register`
   - Method: `POST`
   - Content-Type: `application/json`

3. **Request Validation**
   - Validates JSON body is present
   - Extracts required fields: uid, uname, password, email, phone
   - Delegates validation to auth_service.register_user()
   - Validates field formats (email, password length, etc.)
   - Checks for duplicate username/email

4. **Error Handling**
   - Missing JSON body: 400 with VALIDATION_ERROR
   - Missing required fields: 400 with VALIDATION_ERROR
   - Invalid field formats: 400 with VALIDATION_ERROR
   - Duplicate user: 409 with DUPLICATE_USER
   - Internal errors: 500 with INTERNAL_ERROR
   - All errors include timestamp and error code

5. **Response Formatting**
   - Success response (200):
     ```json
     {
       "status": "success",
       "message": "Registration successful"
     }
     ```
   - Error response (400/409/500):
     ```json
     {
       "status": "error",
       "message": "Error description",
       "code": "ERROR_CODE",
       "timestamp": "ISO 8601 timestamp"
     }
     ```

## Requirements Coverage

### Requirement 1.1: Field Validation
✓ Validates all required fields (uid, uname, password, email, phone) are provided
✓ Returns validation error if any field is missing

### Requirement 1.5: Redirect on Success
✓ Returns success response (frontend will handle redirect)
✓ Status code 200 indicates successful registration

### Requirement 1.6: Duplicate User Rejection
✓ Checks for duplicate username or email via auth_service
✓ Returns 409 status code with DUPLICATE_USER error code
✓ Returns descriptive error message

## Integration with Existing Services

The endpoint integrates with:

1. **auth_service.register_user()** - Handles registration logic
   - Validates all fields
   - Checks for duplicates
   - Hashes password
   - Creates user with initial balance of 100000

2. **Database (via db.py)** - Connection pool management
   - Initialized on app startup
   - Handles SSL connection to AIVEN MySQL
   - Provides error handling for connection failures

## API Usage Example

### Successful Registration

**Request:**
```bash
POST /api/register
Content-Type: application/json

{
  "uid": "user001",
  "uname": "johndoe",
  "password": "securepass123",
  "email": "john@example.com",
  "phone": "1234567890"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Registration successful"
}
```

### Validation Error

**Request:**
```bash
POST /api/register
Content-Type: application/json

{
  "uid": "user002",
  "uname": "janedoe",
  "password": "short"
}
```

**Response (400):**
```json
{
  "status": "error",
  "message": "All fields are required: uid, uname, password, email, phone",
  "code": "VALIDATION_ERROR",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

### Duplicate User Error

**Request:**
```bash
POST /api/register
Content-Type: application/json

{
  "uid": "user003",
  "uname": "johndoe",
  "password": "password123",
  "email": "different@example.com",
  "phone": "9876543210"
}
```

**Response (409):**
```json
{
  "status": "error",
  "message": "Username or email already exists",
  "code": "DUPLICATE_USER",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

## Testing

### Unit Tests (test_app_register.py)

The test suite includes:

1. ✓ test_register_valid_data - Valid registration succeeds
2. ✓ test_register_missing_json - Missing JSON body returns 400
3. ✓ test_register_missing_fields - Missing fields returns 400
4. ✓ test_register_invalid_email - Invalid email format returns 400
5. ✓ test_register_short_password - Short password returns 400
6. ✓ test_register_duplicate_username - Duplicate username returns 409
7. ✓ test_register_duplicate_email - Duplicate email returns 409

**Note:** Tests require database connectivity. Use verify_app.py for structure verification without database.

### Verification Script (verify_app.py)

Verifies:
- Flask app is properly created
- Routes are registered correctly
- /api/register endpoint exists with POST method
- Register function is properly defined

## Running the Application

### Development Mode

```bash
# Ensure .env file is configured with DATABASE_URL
python backend/app.py
```

The application will start on `http://0.0.0.0:5000`

### Production Mode

For production deployment:
1. Set FLASK_ENV=production in .env
2. Use a production WSGI server (gunicorn, uwsgi)
3. Configure proper SSL/TLS certificates
4. Set secure JWT_SECRET_KEY

## Next Steps

Task 7.1 is complete. The next tasks are:

- **Task 7.2**: Implement POST /api/login endpoint
- **Task 7.3**: Implement GET /api/balance endpoint

## Notes

- The implementation follows RESTful API design principles
- Error responses include timestamps for debugging
- All errors are logged for monitoring
- The endpoint is stateless and thread-safe
- Password hashing is handled by auth_service (bcrypt with cost factor 10)
- Initial balance is set to 100000 as per requirements
