# Design Document: kodbank1 Banking Application

## Overview

kodbank1 is a full-stack web banking application built with a three-tier architecture: a frontend client, a backend API server, and a MySQL database. The system implements JWT-based authentication for secure session management and provides core banking operations starting with user registration and balance inquiry.

The application follows a RESTful API design pattern with stateless authentication using JWT tokens stored both client-side (as HTTP-only cookies) and server-side (in the database for validation and revocation capabilities).

## Architecture

### System Components

```
┌─────────────────┐
│   Frontend      │
│   (Browser)     │
│  - Registration │
│  - Login        │
│  - Dashboard    │
└────────┬────────┘
         │ HTTPS
         │ (JWT Cookie)
         ▼
┌─────────────────┐
│   Backend API   │
│   Server        │
│  - Auth Service │
│  - User Service │
│  - JWT Service  │
└────────┬────────┘
         │ MySQL/SSL
         ▼
┌─────────────────┐
│  AIVEN MySQL    │
│   Database      │
│  - kodusers     │
│  - CJWT         │
└─────────────────┘
```

### Technology Stack

**Frontend:**
- HTML5/CSS3/JavaScript (or React/Vue.js for enhanced UX)
- Fetch API or Axios for HTTP requests
- Animation library (e.g., canvas-confetti for celebration effects)

**Backend:**
- Node.js with Express.js (recommended) 
- JWT library (jsonwebtoken for Node.js, PyJWT for Python)
- MySQL client library (mysql2 for Node.js, mysql-connector-python for Python)
- bcrypt for password hashing

**Database:**
- AIVEN MySQL 8.0+
- SSL/TLS encryption enabled

### Communication Flow

1. **Registration Flow**: Frontend → Backend → Database → Backend → Frontend (redirect to login)
2. **Login Flow**: Frontend → Backend → Database (validate) → Database (store token) → Backend (set cookie) → Frontend (redirect to dashboard)
3. **Balance Check Flow**: Frontend (with cookie) → Backend (validate JWT) → Database (fetch balance) → Backend → Frontend (display with animation)

## Components and Interfaces

### Frontend Components

#### 1. Registration Page Component

**Responsibilities:**
- Render registration form with fields: uid, uname, password, email, phone
- Validate input fields client-side (non-empty, email format, phone format)
- Submit registration data to backend API
- Handle success/error responses
- Redirect to login page on success

**Interface:**
```javascript
// API Call
POST /api/register
Content-Type: application/json

Request Body:
{
  "uid": string,
  "uname": string,
  "password": string,
  "email": string,
  "phone": string
}

Response (Success):
{
  "status": "success",
  "message": "Registration successful"
}

Response (Error):
{
  "status": "error",
  "message": string
}
```

#### 2. Login Page Component

**Responsibilities:**
- Render login form with username and password fields
- Submit credentials to backend API
- Store JWT token (handled automatically via cookie)
- Redirect to dashboard on success
- Display error messages on failure

**Interface:**
```javascript
// API Call
POST /api/login
Content-Type: application/json

Request Body:
{
  "username": string,
  "password": string
}

Response (Success):
{
  "status": "success",
  "message": "Login successful"
}
// JWT token set as HTTP-only cookie

Response (Error):
{
  "status": "error",
  "message": string
}
```

#### 3. Dashboard Component

**Responsibilities:**
- Display "Check Balance" button
- Send balance request with JWT token (from cookie)
- Display balance message: "Your balance is : ${balance}"
- Trigger celebration animation on balance display
- Handle authentication errors (redirect to login)

**Interface:**
```javascript
// API Call
GET /api/balance
Cookie: jwt=<token>

Response (Success):
{
  "status": "success",
  "balance": number
}

Response (Error):
{
  "status": "error",
  "message": string
}
```

### Backend Components

#### 1. Authentication Service

**Responsibilities:**
- Validate user credentials against database
- Generate JWT tokens with username (subject) and role (claim)
- Store JWT tokens in CJWT table
- Set JWT token as HTTP-only cookie
- Verify and validate JWT tokens from requests

**Key Functions:**

```typescript
interface AuthService {
  // Register new user
  registerUser(userData: UserRegistrationData): Promise<Result>
  
  // Authenticate user and generate JWT
  login(username: string, password: string): Promise<LoginResult>
  
  // Verify JWT token validity
  verifyToken(token: string): Promise<TokenPayload | null>
  
  // Extract username from valid token
  extractUsername(token: string): string
}

interface UserRegistrationData {
  uid: string
  uname: string
  password: string
  email: string
  phone: string
}

interface LoginResult {
  success: boolean
  token?: string
  message: string
}

interface TokenPayload {
  sub: string      // username
  role: string     // user role
  iat: number      // issued at
  exp: number      // expiration
}
```

**JWT Token Structure:**
```json
{
  "sub": "username",
  "role": "customer",
  "iat": 1234567890,
  "exp": 1234571490
}
```

**Token Generation Algorithm:**
- Use HS256 (HMAC with SHA-256) or RS256 (RSA with SHA-256)
- Generate secure random signing key (minimum 256 bits for HS256)
- Set expiration time (recommended: 1 hour for access tokens)
- Sign token with secret key

#### 2. User Service

**Responsibilities:**
- Create new user records in database
- Fetch user information by username
- Retrieve user balance
- Hash passwords before storage
- Validate password hashes during login

**Key Functions:**

```typescript
interface UserService {
  // Create new user with initial balance
  createUser(userData: UserRegistrationData): Promise<Result>
  
  // Get user by username
  getUserByUsername(username: string): Promise<User | null>
  
  // Get user balance
  getBalance(username: string): Promise<number>
  
  // Verify password
  verifyPassword(plainPassword: string, hashedPassword: string): Promise<boolean>
  
  // Check if username or email exists
  userExists(username: string, email: string): Promise<boolean>
}

interface User {
  uid: string
  username: string
  email: string
  password: string  // hashed
  balance: number
  phone: string
}
```

#### 3. JWT Service

**Responsibilities:**
- Generate JWT tokens
- Store tokens in CJWT table
- Validate token signatures
- Check token expiration
- Retrieve tokens from database

**Key Functions:**

```typescript
interface JWTService {
  // Generate new JWT token
  generateToken(username: string, role: string): string
  
  // Store token in database
  storeToken(token: string, uid: string, expiry: Date): Promise<Result>
  
  // Validate token signature and expiration
  validateToken(token: string): Promise<boolean>
  
  // Decode token payload
  decodeToken(token: string): TokenPayload | null
  
  // Check if token exists in database
  tokenExists(token: string): Promise<boolean>
}
```

### Database Schema

#### Table: kodusers

```sql
CREATE TABLE kodusers (
  uid VARCHAR(50) PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,  -- bcrypt hash
  balance DECIMAL(15, 2) NOT NULL DEFAULT 1000002.00,
  phone VARCHAR(20) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_username (username),
  INDEX idx_email (email)
);
```

#### Table: CJWT

```sql
CREATE TABLE CJWT (
  id INT AUTO_INCREMENT PRIMARY KEY,
  token TEXT NOT NULL,
  uid VARCHAR(50) NOT NULL,
  expiry DATETIME NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (uid) REFERENCES kodusers(uid) ON DELETE CASCADE,
  INDEX idx_uid (uid),
  INDEX idx_expiry (expiry)
);
```

### API Endpoints

#### POST /api/register

**Purpose:** Register a new user account

**Request:**
```json
{
  "uid": "string",
  "uname": "string",
  "password": "string",
  "email": "string",
  "phone": "string"
}
```

**Process:**
1. Validate all required fields are present
2. Check if username or email already exists
3. Hash password using bcrypt (cost factor: 10)
4. Insert user record with initial balance 1000002
5. Return success response

**Response:**
```json
{
  "status": "success|error",
  "message": "string"
}
```

#### POST /api/login

**Purpose:** Authenticate user and establish session

**Request:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Process:**
1. Fetch user record by username
2. Verify password hash matches
3. Generate JWT token (username as subject, role as claim)
4. Store token in CJWT table with expiry
5. Set token as HTTP-only, Secure, SameSite cookie
6. Return success response

**Response:**
```json
{
  "status": "success|error",
  "message": "string"
}
```

**Cookie:**
```
Set-Cookie: jwt=<token>; HttpOnly; Secure; SameSite=Strict; Max-Age=3600
```

#### GET /api/balance

**Purpose:** Retrieve authenticated user's account balance

**Request:**
- JWT token in cookie

**Process:**
1. Extract JWT token from cookie
2. Verify token signature
3. Check token expiration
4. Verify token exists in CJWT table
5. Extract username from token payload
6. Fetch balance from kodusers table
7. Return balance

**Response:**
```json
{
  "status": "success|error",
  "balance": number,
  "message": "string"
}
```

## Data Models

### User Model

```typescript
interface User {
  uid: string           // Unique identifier
  username: string      // Unique username
  email: string         // Unique email address
  password: string      // Bcrypt hashed password
  balance: number       // Account balance (default: 1000002)
  phone: string         // Phone number
  createdAt: Date       // Registration timestamp
}
```

**Validation Rules:**
- uid: Non-empty string, max 50 characters
- username: Non-empty string, max 50 characters, alphanumeric with underscores
- email: Valid email format, max 100 characters
- password: Minimum 8 characters (before hashing)
- phone: Valid phone format, max 20 characters
- balance: Non-negative decimal number

### JWT Token Model

```typescript
interface JWTToken {
  id: number            // Auto-increment primary key
  token: string         // JWT token string
  uid: string           // User ID (foreign key)
  expiry: Date          // Token expiration timestamp
  createdAt: Date       // Token creation timestamp
}
```

**Token Payload:**
```typescript
interface TokenPayload {
  sub: string           // Subject (username)
  role: string          // User role (always "customer")
  iat: number           // Issued at (Unix timestamp)
  exp: number           // Expiration (Unix timestamp)
}
```

### Registration Request Model

```typescript
interface RegistrationRequest {
  uid: string
  uname: string
  password: string
  email: string
  phone: string
}
```

### Login Request Model

```typescript
interface LoginRequest {
  username: string
  password: string
}
```

### API Response Models

```typescript
interface SuccessResponse {
  status: "success"
  message: string
  data?: any
}

interface ErrorResponse {
  status: "error"
  message: string
  code?: string
}

interface BalanceResponse {
  status: "success"
  balance: number
}
```

## Data Flow Examples

### Registration Flow

```
User → Frontend: Fill registration form
Frontend → Backend: POST /api/register {uid, uname, password, email, phone}
Backend → Database: Check if username/email exists
Database → Backend: Not exists
Backend → Backend: Hash password with bcrypt
Backend → Database: INSERT INTO kodusers (uid, username, email, password, balance, phone) VALUES (...)
Database → Backend: Success
Backend → Frontend: {status: "success", message: "Registration successful"}
Frontend → User: Redirect to login page
```

### Login Flow

```
User → Frontend: Enter username and password
Frontend → Backend: POST /api/login {username, password}
Backend → Database: SELECT * FROM kodusers WHERE username = ?
Database → Backend: User record
Backend → Backend: Verify password hash
Backend → Backend: Generate JWT token (sub: username, role: customer)
Backend → Database: INSERT INTO CJWT (token, uid, expiry) VALUES (...)
Database → Backend: Success
Backend → Frontend: Set-Cookie: jwt=<token>; {status: "success"}
Frontend → User: Redirect to dashboard
```

### Balance Check Flow

```
User → Frontend: Click "Check Balance" button
Frontend → Backend: GET /api/balance (Cookie: jwt=<token>)
Backend → Backend: Extract token from cookie
Backend → Backend: Verify token signature
Backend → Backend: Check token expiration
Backend → Database: SELECT * FROM CJWT WHERE token = ?
Database → Backend: Token record found
Backend → Backend: Decode token, extract username
Backend → Database: SELECT balance FROM kodusers WHERE username = ?
Database → Backend: Balance value
Backend → Frontend: {status: "success", balance: 1000002}
Frontend → Frontend: Display "Your balance is : 1000002"
Frontend → User: Show celebration animation
```


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: Complete User Registration

*For any* valid registration request with all required fields (uid, uname, password, email, phone), the system should create a user record in the kodusers table containing all provided fields, with the role set to "customer" and initial balance set to 1000002.

**Validates: Requirements 1.1, 1.2, 1.3, 1.4**

### Property 2: Duplicate User Rejection

*For any* username or email that already exists in the kodusers table, attempting to register a new user with that username or email should be rejected with an error message, and no new user record should be created.

**Validates: Requirements 1.6**

### Property 3: Password Hashing on Registration

*For any* user registration, the password stored in the kodusers table should be a bcrypt hash and not the plaintext password provided during registration.

**Validates: Requirements 6.1**

### Property 4: Valid Credential Authentication

*For any* registered user, submitting correct username and password credentials should result in successful authentication, while submitting incorrect credentials should result in authentication failure.

**Validates: Requirements 2.1, 2.8, 6.2**

### Property 5: JWT Token Structure

*For any* successful login, the generated JWT token should contain the username as the subject claim and "customer" as the role claim, and the token signature should be verifiable using standard JWT validation.

**Validates: Requirements 2.2, 2.3, 6.4**

### Property 6: JWT Token Persistence

*For any* successful login, the generated JWT token should be stored in the CJWT table with the user's uid and an expiry timestamp, and the token should be returned to the client as an HTTP-only cookie.

**Validates: Requirements 2.4, 2.5**

### Property 7: Token Expiration Enforcement

*For any* JWT token, if the current time is after the token's expiry time, then any request using that token should be rejected with an authentication error.

**Validates: Requirements 3.9, 5.3, 5.5**

### Property 8: Token Signature Validation

*For any* JWT token with an invalid or tampered signature, the backend should reject the token and return an authentication error.

**Validates: Requirements 5.4**

### Property 9: Token Expiry Recording

*For any* JWT token generated and stored in the CJWT table, the expiry field should contain a timestamp in the future (relative to token creation time).

**Validates: Requirements 5.1, 5.2**

### Property 10: Authenticated Balance Retrieval

*For any* authenticated user with a valid JWT token, requesting their balance should return the exact balance value stored in the kodusers table for that username.

**Validates: Requirements 3.3, 3.4, 3.5, 3.6**

### Property 11: Unauthenticated Balance Rejection

*For any* balance request with an invalid, expired, or missing JWT token, the backend should reject the request and return an authentication error without revealing any balance information.

**Validates: Requirements 3.9**

### Property 12: No Sensitive Data Exposure

*For any* API response from the backend, the response body should not contain database credentials, JWT signing keys, or other sensitive configuration values.

**Validates: Requirements 6.5**

## Error Handling

### Error Categories

1. **Validation Errors**: Invalid input data (missing fields, invalid formats)
2. **Authentication Errors**: Invalid credentials, expired tokens, invalid signatures
3. **Authorization Errors**: Insufficient permissions (future use)
4. **Database Errors**: Connection failures, query errors, constraint violations
5. **System Errors**: Unexpected server errors

### Error Response Format

All errors should follow a consistent format:

```json
{
  "status": "error",
  "message": "Human-readable error message",
  "code": "ERROR_CODE",
  "timestamp": "ISO 8601 timestamp"
}
```

### Error Codes

- `VALIDATION_ERROR`: Input validation failed
- `DUPLICATE_USER`: Username or email already exists
- `INVALID_CREDENTIALS`: Username or password incorrect
- `TOKEN_EXPIRED`: JWT token has expired
- `TOKEN_INVALID`: JWT token signature invalid or malformed
- `TOKEN_MISSING`: No JWT token provided
- `UNAUTHORIZED`: Authentication required
- `DATABASE_ERROR`: Database operation failed
- `INTERNAL_ERROR`: Unexpected server error

### Error Handling Strategies

#### Registration Errors

- **Missing Fields**: Return `VALIDATION_ERROR` with list of missing fields
- **Invalid Email Format**: Return `VALIDATION_ERROR` with message about email format
- **Duplicate Username/Email**: Return `DUPLICATE_USER` with specific field that's duplicated
- **Database Error**: Return `DATABASE_ERROR` and log full error server-side

#### Login Errors

- **Invalid Credentials**: Return `INVALID_CREDENTIALS` (don't specify if username or password is wrong for security)
- **Database Error**: Return `DATABASE_ERROR` and log full error server-side
- **Token Generation Error**: Return `INTERNAL_ERROR` and log full error server-side

#### Balance Request Errors

- **Missing Token**: Return `TOKEN_MISSING` with 401 status code
- **Expired Token**: Return `TOKEN_EXPIRED` with 401 status code
- **Invalid Token**: Return `TOKEN_INVALID` with 401 status code
- **User Not Found**: Return `UNAUTHORIZED` (token valid but user doesn't exist)
- **Database Error**: Return `DATABASE_ERROR` and log full error server-side

#### Database Connection Errors

- **Connection Failure on Startup**: Log error with full details and exit process with non-zero code
- **Connection Lost During Operation**: Attempt reconnection with exponential backoff, return `DATABASE_ERROR` to client

### Logging Strategy

- **Info Level**: Successful operations (registration, login, balance checks)
- **Warning Level**: Failed authentication attempts, validation errors
- **Error Level**: Database errors, token generation failures, unexpected errors
- **Debug Level**: Detailed request/response data (excluding sensitive fields)

**Never Log:**
- Plaintext passwords
- JWT tokens
- Database credentials
- Full user records (log user IDs only)

## Testing Strategy

### Overview

The testing strategy employs a dual approach combining unit tests for specific examples and edge cases with property-based tests for universal correctness properties. This ensures both concrete behavior validation and comprehensive input coverage.

### Property-Based Testing

Property-based testing will be used to verify the universal correctness properties defined in this document. Each property will be implemented as an automated test that generates random inputs and verifies the property holds across all generated cases.

**Testing Library:**
- For Node.js/TypeScript: **fast-check**
- For Python: **Hypothesis**

**Configuration:**
- Minimum 100 iterations per property test
- Each test must reference its design document property
- Tag format: `Feature: kodbank1, Property {number}: {property_text}`

**Property Test Coverage:**

1. **Property 1 - Complete User Registration**: Generate random valid registration data, verify all fields stored correctly with role="customer" and balance=1000002
2. **Property 2 - Duplicate User Rejection**: Register user, attempt duplicate registration with same username/email, verify rejection
3. **Property 3 - Password Hashing**: Generate random passwords, register users, verify stored passwords are bcrypt hashes
4. **Property 4 - Valid Credential Authentication**: Generate random users, register them, verify login succeeds with correct credentials and fails with incorrect ones
5. **Property 5 - JWT Token Structure**: Generate random users, login, decode JWT, verify structure contains username and role
6. **Property 6 - JWT Token Persistence**: Generate random users, login, verify token stored in CJWT table and returned as cookie
7. **Property 7 - Token Expiration Enforcement**: Generate expired tokens, verify they're rejected
8. **Property 8 - Token Signature Validation**: Generate tokens with invalid signatures, verify they're rejected
9. **Property 9 - Token Expiry Recording**: Generate random users, login, verify CJWT.expiry is in the future
10. **Property 10 - Authenticated Balance Retrieval**: Generate random users with different balances, verify balance requests return correct values
11. **Property 11 - Unauthenticated Balance Rejection**: Generate invalid/expired/missing tokens, verify balance requests are rejected
12. **Property 12 - No Sensitive Data Exposure**: Make various API requests, verify responses don't contain credentials or keys

### Unit Testing

Unit tests will focus on specific examples, edge cases, and integration points between components.

**Test Categories:**

#### 1. Registration Tests
- Valid registration with all fields
- Registration with missing fields (each field individually)
- Registration with invalid email format
- Registration with invalid phone format
- Registration with duplicate username
- Registration with duplicate email
- Registration with very long field values
- Registration with special characters in fields

#### 2. Login Tests
- Successful login with valid credentials
- Login with non-existent username
- Login with incorrect password
- Login with empty username
- Login with empty password
- Login with SQL injection attempts
- Multiple failed login attempts (rate limiting if implemented)

#### 3. Balance Check Tests
- Balance check with valid token
- Balance check with expired token
- Balance check with malformed token
- Balance check with token for non-existent user
- Balance check without token
- Balance check with tampered token

#### 4. JWT Service Tests
- Token generation with valid data
- Token validation with valid token
- Token validation with expired token
- Token validation with invalid signature
- Token decoding with valid token
- Token decoding with malformed token

#### 5. Database Tests
- Successful connection with valid credentials
- Connection failure with invalid credentials
- Query execution with valid data
- Query execution with constraint violations
- Transaction rollback on error

#### 6. Password Hashing Tests
- Hash generation produces different hashes for same password
- Hash verification succeeds with correct password
- Hash verification fails with incorrect password
- Hash strength (bcrypt cost factor verification)

### Integration Testing

Integration tests will verify end-to-end flows across multiple components.

**Test Scenarios:**

1. **Complete Registration Flow**: Frontend → Backend → Database → Response → Redirect
2. **Complete Login Flow**: Frontend → Backend → Database (validate) → Database (store token) → Response with cookie → Redirect
3. **Complete Balance Check Flow**: Frontend with cookie → Backend (validate token) → Database (fetch balance) → Response → Display with animation

### Test Data Management

**Test Database:**
- Use separate test database instance
- Reset database state before each test suite
- Use database transactions for test isolation where possible

**Test Data Generation:**
- Use faker libraries for realistic test data
- Generate edge cases (empty strings, very long strings, special characters)
- Generate boundary values (minimum/maximum lengths)

**Test User Accounts:**
- Create fixture users with known credentials for integration tests
- Generate random users for property-based tests
- Clean up test users after test completion

### Continuous Integration

- Run all tests on every commit
- Fail build if any test fails
- Generate code coverage reports (target: >80% coverage)
- Run property tests with increased iterations (1000+) in CI environment

### Performance Testing

While not the primary focus, basic performance benchmarks should be established:

- Registration endpoint: < 500ms response time
- Login endpoint: < 300ms response time
- Balance check endpoint: < 200ms response time
- Database queries: < 100ms execution time

### Security Testing

- SQL injection attempts in all input fields
- XSS attempts in text fields
- JWT token tampering attempts
- Brute force login attempts
- CSRF protection verification (if implemented)
- SSL/TLS connection verification
