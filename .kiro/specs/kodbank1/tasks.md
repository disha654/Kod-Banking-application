# Implementation Plan: kodbank1 Banking Application

## Overview

This implementation plan breaks down the kodbank1 banking application into discrete coding tasks. The application will be built using Python with Flask for the backend API, MySQL for the database, and vanilla JavaScript for the frontend. Each task builds incrementally on previous work, with testing integrated throughout to validate correctness early.

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create project directory structure (backend/, frontend/, tests/)
  - Create requirements.txt with dependencies: Flask, PyJWT, bcrypt, mysql-connector-python, python-dotenv
  - Create .env file for configuration (database URL, JWT secret key)
  - Create .gitignore to exclude .env and virtual environment
  - Set up virtual environment and install dependencies
  - _Requirements: 4.1_

- [ ] 2. Initialize database schema and connection
  - [x] 2.1 Create database connection module
    - Write db.py with connection pool setup for AIVEN MySQL
    - Implement SSL mode configuration as required by connection string
    - Add connection error handling and logging
    - _Requirements: 4.1, 4.2, 4.5_
  
  - [x] 2.2 Create database schema initialization script
    - Write schema.sql with CREATE TABLE statements for kodusers and CJWT
    - Add indexes for username, email, uid, and expiry fields
    - Create init_db.py script to execute schema creation
    - _Requirements: 4.3, 4.4_
  
  - [ ]* 2.3 Write unit tests for database connection
    - Test successful connection with valid credentials
    - Test connection failure handling with invalid credentials
    - _Requirements: 4.1, 4.5_

- [ ] 3. Implement user service and password hashing
  - [x] 3.1 Create user service module
    - Write user_service.py with functions: create_user, get_user_by_username, user_exists, get_balance
    - Implement bcrypt password hashing (cost factor: 10)
    - Implement password verification function
    - Add input validation for all user fields
    - _Requirements: 1.1, 1.4, 6.1, 6.2_
  
  - [ ]* 3.2 Write property test for password hashing
    - **Property 3: Password Hashing on Registration**
    - **Validates: Requirements 6.1**
    - Generate random passwords, verify stored passwords are bcrypt hashes
  
  - [ ]* 3.3 Write property test for complete user registration
    - **Property 1: Complete User Registration**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4**
    - Generate random registration data, verify all fields stored with role="customer" and balance=1000002
  
  - [ ]* 3.4 Write property test for duplicate user rejection
    - **Property 2: Duplicate User Rejection**
    - **Validates: Requirements 1.6**
    - Register user, attempt duplicate with same username/email, verify rejection
  
  - [ ]* 3.5 Write unit tests for user service
    - Test user creation with valid data
    - Test user creation with missing fields
    - Test user_exists with existing and non-existing users
    - Test get_balance for existing user
    - _Requirements: 1.1, 1.4, 1.6_

- [ ] 4. Implement JWT service
  - [x] 4.1 Create JWT service module
    - Write jwt_service.py with functions: generate_token, validate_token, decode_token, store_token, token_exists
    - Implement JWT generation with username as subject and role as claim
    - Set token expiration (1 hour)
    - Implement token signature validation
    - Implement token expiration checking
    - _Requirements: 2.2, 2.3, 2.4, 5.1, 5.2, 5.3, 5.4_
  
  - [ ]* 4.2 Write property test for JWT token structure
    - **Property 5: JWT Token Structure**
    - **Validates: Requirements 2.2, 2.3, 6.4**
    - Generate random users, create tokens, decode and verify structure contains username and role
  
  - [ ]* 4.3 Write property test for token expiration enforcement
    - **Property 7: Token Expiration Enforcement**
    - **Validates: Requirements 3.9, 5.3, 5.5**
    - Generate expired tokens, verify they're rejected
  
  - [ ]* 4.4 Write property test for token signature validation
    - **Property 8: Token Signature Validation**
    - **Validates: Requirements 5.4**
    - Generate tokens with invalid signatures, verify they're rejected
  
  - [ ]* 4.5 Write property test for token expiry recording
    - **Property 9: Token Expiry Recording**
    - **Validates: Requirements 5.1, 5.2**
    - Generate tokens, verify CJWT.expiry is in the future
  
  - [ ]* 4.6 Write unit tests for JWT service
    - Test token generation with valid data
    - Test token validation with valid token
    - Test token validation with expired token
    - Test token validation with malformed token
    - Test token storage in CJWT table
    - _Requirements: 2.2, 2.3, 2.4, 5.1, 5.3, 5.4_

- [x] 5. Checkpoint - Ensure core services work
  - Ensure all tests pass, ask the user if questions arise. 

- [ ] 6. Implement authentication service
  - [x] 6.1 Create authentication service module
    - Write auth_service.py with functions: register_user, login, verify_token_from_request
    - Implement registration logic (validate, check duplicates, hash password, create user)
    - Implement login logic (validate credentials, generate JWT, store token)
    - Implement token extraction and verification from requests
    - _Requirements: 1.1, 1.6, 2.1, 2.2, 2.4, 2.8_
  
  - [ ]* 6.2 Write property test for valid credential authentication
    - **Property 4: Valid Credential Authentication**
    - **Validates: Requirements 2.1, 2.8, 6.2**
    - Generate random users, verify login succeeds with correct credentials and fails with incorrect ones
  
  - [ ]* 6.3 Write property test for JWT token persistence
    - **Property 6: JWT Token Persistence**
    - **Validates: Requirements 2.4, 2.5**
    - Generate random users, login, verify token stored in CJWT and returned as cookie
  
  - [ ]* 6.4 Write unit tests for authentication service
    - Test registration with valid data
    - Test registration with duplicate username
    - Test registration with duplicate email
    - Test login with valid credentials
    - Test login with invalid username
    - Test login with invalid password
    - _Requirements: 1.1, 1.6, 2.1, 2.8_

- [ ] 7. Implement Flask API endpoints
  - [x] 7.1 Create Flask application and register endpoint
    - Write app.py with Flask app initialization
    - Implement POST /api/register endpoint
    - Add request validation for required fields
    - Add error handling and response formatting
    - Return success response on successful registration
    - _Requirements: 1.1, 1.5, 1.6_
  
  - [x] 7.2 Implement login endpoint
    - Implement POST /api/login endpoint
    - Add request validation for username and password
    - Call authentication service to validate credentials
    - Set JWT token as HTTP-only, Secure, SameSite cookie
    - Return success response on successful login
    - Add error handling for invalid credentials
    - _Requirements: 2.1, 2.5, 2.6, 2.8_
  
  - [x] 7.3 Implement balance endpoint
    - Implement GET /api/balance endpoint
    - Extract JWT token from cookie
    - Validate token using authentication service
    - Extract username from token
    - Fetch balance using user service
    - Return balance in response
    - Add error handling for invalid/expired tokens
    - _Requirements: 3.2, 3.3, 3.4, 3.5, 3.6, 3.9_
  
  - [ ]* 7.4 Write property test for authenticated balance retrieval
    - **Property 10: Authenticated Balance Retrieval**
    - **Validates: Requirements 3.3, 3.4, 3.5, 3.6**
    - Generate random users with different balances, verify balance requests return correct values
  
  - [ ]* 7.5 Write property test for unauthenticated balance rejection
    - **Property 11: Unauthenticated Balance Rejection**
    - **Validates: Requirements 3.9**
    - Generate invalid/expired/missing tokens, verify balance requests are rejected
  
  - [ ]* 7.6 Write property test for no sensitive data exposure
    - **Property 12: No Sensitive Data Exposure**
    - **Validates: Requirements 6.5**
    - Make various API requests, verify responses don't contain credentials or keys
  
  - [ ]* 7.7 Write unit tests for API endpoints
    - Test /api/register with valid data
    - Test /api/register with missing fields
    - Test /api/register with duplicate user
    - Test /api/login with valid credentials
    - Test /api/login with invalid credentials
    - Test /api/balance with valid token
    - Test /api/balance with invalid token
    - Test /api/balance without token
    - _Requirements: 1.1, 1.5, 1.6, 2.1, 2.6, 2.8, 3.2, 3.6, 3.9_

- [x] 8. Checkpoint - Ensure backend API works
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implement frontend registration page
  - [x] 9.1 Create HTML structure for registration page
    - Create frontend/register.html with form fields: uid, uname, password, email, phone
    - Add form validation attributes (required, email type, etc.)
    - Add submit button
    - Include link to login page
    - _Requirements: 1.1_
  
  - [x] 9.2 Create JavaScript for registration functionality
    - Create frontend/js/register.js
    - Add form submit event handler
    - Implement client-side validation
    - Send POST request to /api/register with form data
    - Handle success response (redirect to login page)
    - Handle error response (display error message)
    - _Requirements: 1.1, 1.5, 1.6_
  
  - [x] 9.3 Create CSS for registration page styling
    - Create frontend/css/styles.css
    - Style registration form with clean, professional design
    - Add responsive design for mobile devices
    - Style error messages

- [ ] 10. Implement frontend login page
  - [x] 10.1 Create HTML structure for login page
    - Create frontend/login.html with form fields: username, password
    - Add submit button
    - Include link to registration page
    - _Requirements: 2.1_
  
  - [x] 10.2 Create JavaScript for login functionality
    - Create frontend/js/login.js
    - Add form submit event handler
    - Send POST request to /api/login with credentials
    - Handle success response (redirect to dashboard)
    - Handle error response (display error message)
    - _Requirements: 2.1, 2.6, 2.7, 2.8_
  
  - [x] 10.3 Style login page
    - Add CSS styling for login form
    - Match registration page design
    - Style error messages

- [ ] 11. Implement frontend dashboard page
  - [x] 11.1 Create HTML structure for dashboard page
    - Create frontend/dashboard.html
    - Add "Check Balance" button
    - Add container for balance display message
    - Add container for celebration animation
    - _Requirements: 3.1_
  
  - [x] 11.2 Create JavaScript for dashboard functionality
    - Create frontend/js/dashboard.js
    - Add click event handler for "Check Balance" button
    - Send GET request to /api/balance (cookie sent automatically)
    - Handle success response (display balance message)
    - Display message: "Your balance is : ${balance}"
    - Handle error response (redirect to login if unauthorized)
    - _Requirements: 3.2, 3.6, 3.7, 3.9_
  
  - [x] 11.3 Implement celebration animation
    - Add canvas-confetti library or create custom animation
    - Trigger animation when balance is displayed
    - Create visually appealing celebration effect
    - _Requirements: 3.8_
  
  - [x] 11.4 Style dashboard page
    - Add CSS styling for dashboard
    - Style "Check Balance" button
    - Style balance display message
    - Add background styling for animation

- [ ] 12. Add CORS and security middleware
  - [x] 12.1 Configure CORS for Flask app
    - Install flask-cors
    - Configure CORS to allow frontend origin
    - Set credentials: true for cookie support
  
  - [x] 12.2 Add security headers
    - Add helmet-like security headers
    - Configure Content-Security-Policy
    - Add X-Content-Type-Options, X-Frame-Options headers
  
  - [x] 12.3 Configure cookie security
    - Ensure cookies are HTTP-only
    - Set Secure flag (requires HTTPS)
    - Set SameSite=Strict
    - _Requirements: 2.5, 6.3_

- [ ] 13. Create application configuration and environment setup
  - [x] 13.1 Create configuration module
    - Write config.py to load environment variables
    - Define configuration for database URL, JWT secret, token expiry
    - Add validation for required environment variables
    - _Requirements: 4.1, 5.1_
  
  - [x] 13.2 Create example environment file
    - Create .env.example with placeholder values
    - Document all required environment variables
    - Add instructions for setup
  
  - [x] 13.3 Create application entry point
    - Create run.py to start Flask application
    - Add development/production mode configuration
    - Add logging configuration
    - _Requirements: 4.5_

- [ ] 14. Integration and wiring
  - [x] 14.1 Wire all components together
    - Ensure Flask app imports all endpoints
    - Verify database connection on startup
    - Test complete registration flow
    - Test complete login flow
    - Test complete balance check flow
    - _Requirements: All_
  
  - [ ]* 14.2 Write integration tests
    - Test complete registration → login → balance check flow
    - Test error flows (invalid registration → login with wrong password → balance without auth)
    - Test session persistence across requests
    - _Requirements: All_

- [ ] 15. Create documentation and setup instructions
  - [x] 15.1 Create README.md
    - Document project structure
    - Add setup instructions (virtual environment, dependencies, database)
    - Add configuration instructions (.env file)
    - Add instructions to run the application
    - Document API endpoints
  
  - [x] 15.2 Create API documentation
    - Document all endpoints with request/response examples
    - Document error codes and messages
    - Document authentication flow
  
  - [x] 15.3 Add code comments and docstrings
    - Add docstrings to all functions and classes
    - Add inline comments for complex logic
    - Document security considerations

- [x] 16. Final checkpoint - Ensure all tests pass
  - Run all unit tests and property tests
  - Run integration tests
  - Verify all requirements are met
  - Test application manually end-to-end
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties with minimum 100 iterations
- Unit tests validate specific examples and edge cases
- Integration tests verify end-to-end flows
- Database credentials are provided in the requirements but should be stored in .env file
- JWT secret key should be generated securely and stored in .env file
- The application uses HTTP-only cookies for JWT storage to prevent XSS attacks
- SSL/TLS should be configured for production deployment
