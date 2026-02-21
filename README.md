# kodbank1 Banking Application

A secure web-based banking application with JWT authentication, user registration, and balance inquiry features. Built with Flask (Python) backend and vanilla JavaScript frontend, connected to an AIVEN MySQL database.

## Features

- **User Registration**: Create new banking accounts with secure password hashing
- **JWT Authentication**: Secure login with JSON Web Token-based session management
- **Balance Inquiry**: Check account balance through an authenticated dashboard
- **Security**: HTTP-only cookies, CORS protection, security headers, and SSL database connections

## Project Structure

```
kodbank1/
├── backend/                    # Backend API server
│   ├── app.py                 # Flask application and API endpoints
│   ├── auth_service.py        # Authentication logic (register, login, token verification)
│   ├── user_service.py        # User management (create, fetch, balance)
│   ├── jwt_service.py         # JWT token generation and validation
│   ├── db.py                  # Database connection pool and utilities
│   ├── config.py              # Configuration loader (environment variables)
│   ├── schema.sql             # Database schema (kodusers, CJWT tables)
│   └── init_db.py             # Database initialization script
├── frontend/                   # Frontend client
│   ├── register.html          # User registration page
│   ├── login.html             # User login page
│   ├── dashboard.html         # User dashboard with balance check
│   ├── css/
│   │   └── styles.css         # Application styling
│   └── js/
│       ├── register.js        # Registration functionality
│       ├── login.js           # Login functionality
│       └── dashboard.js       # Dashboard and balance check
├── tests/                      # Test files
├── .env                        # Environment configuration (not in git)
├── .env.example               # Example environment configuration
├── requirements.txt           # Python dependencies
├── run.py                     # Application entry point
└── README.md                  # This file
```

## Technology Stack

**Backend:**
- Python 3.8+
- Flask 3.0.0 - Web framework
- PyJWT 2.8.0 - JWT token handling
- bcrypt 4.1.2 - Password hashing
- mysql-connector-python 8.2.0 - MySQL database driver
- flask-cors 4.0.0 - CORS support
- python-dotenv 1.0.0 - Environment variable management

**Frontend:**
- HTML5/CSS3/JavaScript (vanilla)
- Fetch API for HTTP requests
- canvas-confetti for celebration animations

**Database:**
- AIVEN MySQL 8.0+ with SSL/TLS encryption

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- AIVEN MySQL database account
- Git (optional)

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd kodbank1
```

### 2. Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and update the following values:

```env
# Database Configuration
DATABASE_URL=mysql://avnadmin:YOUR_PASSWORD@mysql-kodbank-project.aivencloud.com:12345/defaultdb?ssl-mode=REQUIRED

# JWT Configuration
JWT_SECRET_KEY=your-generated-secret-key-here
JWT_EXPIRY_HOURS=1

# Application Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

**Generate a secure JWT secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it as your `JWT_SECRET_KEY` value.

### 5. Initialize Database

Run the database initialization script to create the required tables:

```bash
python backend/init_db.py
```

This creates two tables:
- `kodusers`: Stores user account information
- `CJWT`: Stores JWT tokens for session management

### 6. Run the Application

**Option 1: Using run.py (recommended)**
```bash
python run.py
```

**Option 2: Using Flask directly**
```bash
python backend/app.py
```

The application will start on `http://localhost:5000`

### 7. Access the Application

Open your web browser and navigate to:
- Registration: `http://localhost:5000/register.html`
- Login: `http://localhost:5000/login.html`
- Dashboard: `http://localhost:5000/dashboard.html` (requires authentication)

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Register User

**POST** `/api/register`

Register a new user account with an initial balance of 1,000,002.

**Request Body:**
```json
{
  "uid": "user123",
  "uname": "johndoe",
  "password": "securepassword123",
  "email": "john@example.com",
  "phone": "+1234567890"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Registration successful"
}
```

**Error Response (400/409):**
```json
{
  "status": "error",
  "message": "Username already exists",
  "code": "DUPLICATE_USER",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Error Codes:**
- `VALIDATION_ERROR`: Missing or invalid fields
- `DUPLICATE_USER`: Username or email already exists
- `INTERNAL_ERROR`: Server error

---

#### 2. Login

**POST** `/api/login`

Authenticate user and receive JWT token as HTTP-only cookie.

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Login successful"
}
```

Sets JWT token as HTTP-only cookie:
```
Set-Cookie: jwt=<token>; HttpOnly; Secure; SameSite=Strict; Max-Age=3600
```

**Error Response (400/401):**
```json
{
  "status": "error",
  "message": "Invalid credentials",
  "code": "INVALID_CREDENTIALS",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Error Codes:**
- `VALIDATION_ERROR`: Missing username or password
- `INVALID_CREDENTIALS`: Incorrect username or password
- `INTERNAL_ERROR`: Server error

---

#### 3. Get Balance

**GET** `/api/balance`

Retrieve authenticated user's account balance.

**Request:**
- JWT token automatically sent via cookie

**Success Response (200):**
```json
{
  "status": "success",
  "balance": 1000002.00
}
```

**Error Response (401):**
```json
{
  "status": "error",
  "message": "Token expired",
  "code": "TOKEN_EXPIRED",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Error Codes:**
- `TOKEN_MISSING`: No JWT token provided
- `TOKEN_EXPIRED`: JWT token has expired
- `TOKEN_INVALID`: JWT token signature invalid
- `UNAUTHORIZED`: Authentication required
- `INTERNAL_ERROR`: Server error

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | MySQL connection string with SSL | - | Yes |
| `JWT_SECRET_KEY` | Secret key for JWT signing | - | Yes |
| `JWT_EXPIRY_HOURS` | Token expiration time in hours | 1 | No |
| `FLASK_ENV` | Flask environment (development/production) | development | No |
| `FLASK_DEBUG` | Enable Flask debug mode | True | No |

### Database Schema

**kodusers table:**
```sql
CREATE TABLE kodusers (
  uid VARCHAR(50) PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  balance DECIMAL(15, 2) NOT NULL DEFAULT 1000002.00,
  phone VARCHAR(20) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**CJWT table:**
```sql
CREATE TABLE CJWT (
  id INT AUTO_INCREMENT PRIMARY KEY,
  token TEXT NOT NULL,
  uid VARCHAR(50) NOT NULL,
  expiry DATETIME NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (uid) REFERENCES kodusers(uid) ON DELETE CASCADE
);
```

## Security Features

- **Password Hashing**: bcrypt with cost factor 10
- **JWT Tokens**: HS256 algorithm with configurable expiration
- **HTTP-only Cookies**: Prevents XSS attacks
- **Secure Cookies**: HTTPS-only transmission
- **SameSite Cookies**: CSRF protection
- **CORS Configuration**: Restricted origins with credentials support
- **Security Headers**: CSP, X-Frame-Options, X-Content-Type-Options, etc.
- **SSL Database Connection**: Encrypted data transmission

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_user_service.py

# Run with coverage
pytest --cov=backend
```

### Code Structure

- **app.py**: Flask application, API endpoints, middleware
- **auth_service.py**: Registration, login, token verification
- **user_service.py**: User CRUD operations, balance retrieval
- **jwt_service.py**: Token generation, validation, storage
- **db.py**: Database connection pool, query utilities
- **config.py**: Environment configuration loader

## Troubleshooting

### Database Connection Issues

**Error**: "Failed to initialize database"

**Solution**:
1. Verify DATABASE_URL in `.env` is correct
2. Check AIVEN MySQL service is running
3. Ensure SSL mode is set to REQUIRED
4. Verify network connectivity to AIVEN

### JWT Token Issues

**Error**: "Token expired" or "Token invalid"

**Solution**:
1. Check JWT_SECRET_KEY is set in `.env`
2. Verify token hasn't expired (default: 1 hour)
3. Clear browser cookies and login again
4. Ensure system clock is synchronized

### CORS Issues

**Error**: "CORS policy blocked"

**Solution**:
1. Verify frontend origin is in CORS allowed origins
2. Check credentials are enabled in CORS config
3. Ensure cookies are being sent with requests

### Import Errors

**Error**: "ModuleNotFoundError"

**Solution**:
1. Activate virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Verify Python version is 3.8+

## Production Deployment

### Pre-deployment Checklist

- [ ] Set `FLASK_ENV=production` in `.env`
- [ ] Set `FLASK_DEBUG=False` in `.env`
- [ ] Generate strong JWT_SECRET_KEY
- [ ] Use production database credentials
- [ ] Enable HTTPS for secure cookie transmission
- [ ] Configure proper CORS origins
- [ ] Set up logging and monitoring
- [ ] Review security headers configuration
- [ ] Test all endpoints with production settings

### Recommended Production Setup

- Use a production WSGI server (Gunicorn, uWSGI)
- Deploy behind a reverse proxy (Nginx, Apache)
- Enable HTTPS with valid SSL certificate
- Set up database connection pooling
- Implement rate limiting
- Configure log rotation
- Set up automated backups
- Monitor application performance

## License

[Disha V]

## Support

For issues, questions, or contributions, please contact [your-contact-info].
