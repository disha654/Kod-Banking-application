# Requirements Document

## Introduction

kodbank1 is a web-based banking application that enables users to register accounts, authenticate securely using JWT tokens, and check their account balances through an interactive dashboard. The system provides secure user management with role-based access control and persistent session management.

## Glossary

- **System**: The kodbank1 banking application (frontend and backend)
- **User**: A person interacting with the banking application
- **Customer**: A user with the "customer" role
- **JWT_Token**: JSON Web Token used for authentication and authorization
- **Backend**: The server-side component that processes requests and manages data
- **Frontend**: The client-side user interface
- **Database**: The AIVEN MySQL database service storing application data
- **Session**: An authenticated user's active connection identified by a JWT token
- **Balance**: The amount of money in a user's account

## Requirements

### Requirement 1: User Registration

**User Story:** As a new user, I want to register for a banking account, so that I can access banking services.

#### Acceptance Criteria

1. WHEN a user submits registration information, THE System SHALL validate that all required fields (uid, uname, password, email, phone) are provided
2. WHEN a user registers, THE System SHALL assign the role "customer" to the new account
3. WHEN a user completes registration, THE System SHALL create an account with an initial balance of 100000
4. WHEN registration data is validated, THE System SHALL store the user information in the kodusers table with fields (uid, username, email, password, balance, phone)
5. WHEN a user successfully registers, THE System SHALL redirect the user to the login page
6. IF a username or email already exists, THEN THE System SHALL reject the registration and return an error message 

### Requirement 2: User Authentication with JWT

**User Story:** As a registered user, I want to log in securely with my credentials, so that I can access my banking dashboard.

#### Acceptance Criteria

1. WHEN a user submits login credentials (username and password), THE Backend SHALL validate the credentials against the kodusers table
2. WHEN credentials are valid, THE Backend SHALL generate a JWT token with the username as the subject and role as a claim
3. WHEN generating a JWT token, THE Backend SHALL use a standard signature key generation algorithm
4. WHEN a JWT token is generated, THE Backend SHALL store the token in the CJWT table with fields (id, token, uid, expiry)
5. WHEN a JWT token is created, THE Backend SHALL add the token as a cookie to the client response
6. WHEN authentication succeeds, THE Backend SHALL send a success status response to the client
7. WHEN authentication succeeds, THE Frontend SHALL redirect the user to the user dashboard
8. IF credentials are invalid, THEN THE Backend SHALL reject the login attempt and return an error message

### Requirement 3: Balance Inquiry

**User Story:** As an authenticated customer, I want to check my account balance, so that I can monitor my funds.

#### Acceptance Criteria

1. WHEN a user views the dashboard, THE Frontend SHALL display a "Check Balance" button
2. WHEN a user clicks the "Check Balance" button, THE Frontend SHALL send a request to the Backend with the JWT token
3. WHEN the Backend receives a balance request, THE Backend SHALL verify and validate the JWT token
4. WHEN the JWT token is valid, THE Backend SHALL extract the username from the token
5. WHEN the username is extracted, THE Backend SHALL fetch the balance from the kodusers table using the username
6. WHEN the balance is retrieved, THE Backend SHALL send the balance value to the Frontend
7. WHEN the Frontend receives the balance, THE Frontend SHALL display the message "Your balance is : ${balance}"
8. WHEN the balance is displayed, THE Frontend SHALL show a celebratory background animation
9. IF the JWT token is invalid or expired, THEN THE Backend SHALL reject the request and return an authentication error

### Requirement 4: Database Connection and Management

**User Story:** As the system, I want to connect to a secure MySQL database, so that I can persist and retrieve user data reliably.

#### Acceptance Criteria

1. WHEN the Backend starts, THE Backend SHALL establish a connection to the AIVEN MySQL database service using the provided connection URL
2. WHEN connecting to the database, THE Backend SHALL use SSL mode as required by the connection string
3. WHEN the Backend needs to store or retrieve data, THE Backend SHALL use the kodusers table for user information
4. WHEN the Backend needs to manage JWT tokens, THE Backend SHALL use the CJWT table for token storage
5. IF the database connection fails, THEN THE Backend SHALL log the error and prevent application startup

### Requirement 5: Session Management

**User Story:** As the system, I want to manage user sessions securely, so that only authenticated users can access protected resources.

#### Acceptance Criteria

1. WHEN a JWT token is generated, THE Backend SHALL set an appropriate expiry time for the token
2. WHEN storing a JWT token, THE Backend SHALL record the expiry time in the CJWT table
3. WHEN validating a JWT token, THE Backend SHALL check that the token has not expired
4. WHEN validating a JWT token, THE Backend SHALL verify the token signature using the same key used for generation
5. IF a token is expired, THEN THE Backend SHALL reject the request and require re-authentication

### Requirement 6: Security and Data Protection

**User Story:** As a user, I want my password and personal information protected, so that my account remains secure.

#### Acceptance Criteria

1. WHEN a user registers, THE Backend SHALL hash the password before storing it in the database
2. WHEN validating login credentials, THE Backend SHALL compare the hashed password with the stored hash
3. WHEN transmitting sensitive data, THE System SHALL use secure connections (HTTPS for frontend-backend, SSL for database)
4. WHEN generating JWT tokens, THE Backend SHALL use a cryptographically secure signature algorithm
5. THE Backend SHALL NOT expose database credentials or JWT signing keys in client responses
