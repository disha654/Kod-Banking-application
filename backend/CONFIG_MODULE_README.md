# Configuration Module Documentation

## Overview

The `config.py` module provides centralized configuration management for the kodbank1 application. It loads environment variables from the `.env` file, validates required settings, and provides a clean interface for accessing configuration values throughout the application.

## Features

- **Centralized Configuration**: All configuration values in one place
- **Automatic Validation**: Validates required environment variables on module import
- **Type Safety**: Converts environment variables to appropriate types (int, bool, list)
- **Security Checks**: Enforces minimum security requirements (e.g., JWT secret key length)
- **Convenient Accessors**: Helper methods to get configuration by category
- **Environment Detection**: Methods to check if running in production or development

## Requirements

This module satisfies the following requirements:
- **Requirement 4.1**: Database connection configuration
- **Requirement 5.1**: JWT token expiry configuration

## Configuration Variables

### Required Environment Variables

The following environment variables **must** be set in the `.env` file:

| Variable | Description | Validation |
|----------|-------------|------------|
| `DATABASE_URL` | MySQL database connection URL | Must start with `mysql://` |
| `JWT_SECRET_KEY` | Secret key for JWT token signing | Must be at least 32 characters |

### Optional Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_EXPIRY_HOURS` | `1` | JWT token expiration time in hours |
| `FLASK_ENV` | `development` | Flask environment (development/production) |
| `FLASK_DEBUG` | `False` | Enable Flask debug mode |
| `FLASK_HOST` | `0.0.0.0` | Flask server host |
| `FLASK_PORT` | `5000` | Flask server port |
| `CORS_ORIGINS` | See below | Comma-separated list of allowed CORS origins |
| `COOKIE_SECURE` | `True` | Enable secure flag for cookies |

**Default CORS Origins:**
```
http://localhost:3000,http://localhost:5500,http://127.0.0.1:5500,http://127.0.0.1:3000
```

## Usage

### Basic Usage

```python
from config import Config

# Configuration is automatically validated on import
# If validation fails, ConfigurationError is raised

# Access configuration values directly
database_url = Config.DATABASE_URL
jwt_secret = Config.JWT_SECRET_KEY
expiry_hours = Config.JWT_EXPIRY_HOURS
```

### Using Accessor Methods

The Config class provides convenient accessor methods that return configuration dictionaries:

```python
from config import Config

# Get database configuration
db_config = Config.get_database_config()
# Returns: {'url': 'mysql://...'}

# Get JWT configuration
jwt_config = Config.get_jwt_config()
# Returns: {
#     'secret_key': '...',
#     'algorithm': 'HS256',
#     'expiry_hours': 1
# }

# Get Flask configuration
flask_config = Config.get_flask_config()
# Returns: {
#     'env': 'development',
#     'debug': True,
#     'host': '0.0.0.0',
#     'port': 5000
# }

# Get CORS configuration
cors_config = Config.get_cors_config()
# Returns: {
#     'origins': ['http://localhost:3000', ...],
#     'supports_credentials': True
# }

# Get cookie configuration
cookie_config = Config.get_cookie_config()
# Returns: {
#     'secure': True,
#     'httponly': True,
#     'samesite': 'Strict',
#     'max_age': 3600
# }
```

### Environment Detection

```python
from config import Config

# Check if running in production
if Config.is_production():
    # Production-specific logic
    pass

# Check if running in development
if Config.is_development():
    # Development-specific logic
    pass
```

### Manual Validation

```python
from config import Config, ConfigurationError

try:
    Config.validate()
    print("Configuration is valid")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

## Integration with Existing Modules

### Updating db.py

Replace direct environment variable access with Config:

```python
# Before
import os
from dotenv import load_dotenv
load_dotenv()
database_url = os.getenv('DATABASE_URL')

# After
from config import Config
database_url = Config.DATABASE_URL
```

### Updating jwt_service.py

Replace direct environment variable access with Config:

```python
# Before
import os
from dotenv import load_dotenv
load_dotenv()
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_EXPIRY_HOURS = int(os.getenv('JWT_EXPIRY_HOURS', 1))

# After
from config import Config
JWT_SECRET_KEY = Config.JWT_SECRET_KEY
JWT_EXPIRY_HOURS = Config.JWT_EXPIRY_HOURS
```

### Updating app.py

Replace direct configuration with Config:

```python
# Before
app.run(debug=True, host='0.0.0.0', port=5000)

# After
from config import Config
flask_config = Config.get_flask_config()
app.run(
    debug=flask_config['debug'],
    host=flask_config['host'],
    port=flask_config['port']
)
```

## Validation Rules

The configuration module enforces the following validation rules:

1. **DATABASE_URL**:
   - Must be set
   - Must start with `mysql://`

2. **JWT_SECRET_KEY**:
   - Must be set
   - Must be at least 32 characters long (security requirement)

3. **JWT_EXPIRY_HOURS**:
   - Must be a positive integer

4. **FLASK_PORT**:
   - Must be between 1 and 65535

If any validation rule fails, a `ConfigurationError` is raised with a detailed error message.

## Error Handling

```python
from config import Config, ConfigurationError

try:
    # Configuration is validated on import
    from config import Config
except ConfigurationError as e:
    print(f"Configuration error: {e}")
    # Handle error (e.g., exit application)
```

## Testing

Run the configuration tests:

```bash
python -m pytest backend/test_config.py -v
```

Run the configuration demo:

```bash
python backend/demo_config.py
```

## Security Considerations

1. **JWT Secret Key**: The module enforces a minimum length of 32 characters for the JWT secret key to ensure cryptographic security.

2. **Cookie Security**: Default cookie configuration includes:
   - `HttpOnly`: Prevents JavaScript access (XSS protection)
   - `Secure`: Only sent over HTTPS
   - `SameSite=Strict`: CSRF protection

3. **Environment Variables**: Never commit the `.env` file to version control. Use `.env.example` for documentation.

## Example .env File

```env
# Database Configuration
DATABASE_URL=mysql://user:password@host:port/database?ssl-mode=REQUIRED

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-at-least-32-characters-long
JWT_EXPIRY_HOURS=1

# Application Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5500

# Security Configuration
COOKIE_SECURE=True
```

## Benefits

1. **Single Source of Truth**: All configuration in one module
2. **Early Failure**: Configuration errors detected at startup, not runtime
3. **Type Safety**: Automatic type conversion from environment variables
4. **Maintainability**: Easy to add new configuration values
5. **Testability**: Easy to mock configuration in tests
6. **Security**: Enforces security best practices

## Task Completion

This configuration module completes **Task 13.1** from the implementation plan:

- ✅ Write config.py to load environment variables
- ✅ Define configuration for database URL, JWT secret, token expiry
- ✅ Add validation for required environment variables
- ✅ Requirements: 4.1, 5.1
