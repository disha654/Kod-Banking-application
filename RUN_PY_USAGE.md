# run.py - Application Entry Point

## Overview

`run.py` is the main entry point for the kodbank1 banking application. It handles:
- Application startup
- Environment-based configuration (development/production)
- Logging setup
- Flask server initialization

## Usage

### Development Mode (Default)

```bash
python run.py
```

This will start the application with:
- Debug mode enabled
- Detailed logging (DEBUG level)
- Host: 0.0.0.0
- Port: 5000
- Logs written to console and `kodbank1.log`

### Production Mode

Set the environment variable in your `.env` file:

```
FLASK_ENV=production
FLASK_DEBUG=False
```

Then run:

```bash
python run.py
```

This will start the application with:
- Debug mode disabled
- Warning-level logging only
- Secure cookie settings
- Production-optimized configuration

## Configuration

The application reads configuration from the `.env` file through the `Config` class:

- `FLASK_ENV`: Environment mode (development/production)
- `FLASK_DEBUG`: Enable/disable debug mode
- `FLASK_HOST`: Host to bind to (default: 0.0.0.0)
- `FLASK_PORT`: Port to listen on (default: 5000)
- `DATABASE_URL`: MySQL database connection string
- `JWT_SECRET_KEY`: Secret key for JWT token signing

## Logging

### Development Mode
- Log level: DEBUG
- Output: Console (stdout) + kodbank1.log file
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

### Production Mode
- Log level: WARNING
- Output: Console (stdout) + kodbank1.log file
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

## Features

1. **Environment Detection**: Automatically detects development vs production mode
2. **Logging Configuration**: Sets up appropriate logging based on environment
3. **Configuration Validation**: Validates all required environment variables on startup
4. **Database Connection**: Initializes database connection pool before starting server
5. **Error Handling**: Gracefully handles startup errors and exits with appropriate codes

## Requirements

Implements requirement 4.5:
- Create run.py to start Flask application
- Add development/production mode configuration
- Add logging configuration

## Example Output

### Development Mode
```
2024-02-21 16:45:30,123 - __main__ - INFO - Running in DEVELOPMENT mode
2024-02-21 16:45:30,123 - __main__ - INFO - Logging level: DEBUG
2024-02-21 16:45:30,124 - __main__ - INFO - ============================================================
2024-02-21 16:45:30,124 - __main__ - INFO - Starting kodbank1 Banking Application
2024-02-21 16:45:30,124 - __main__ - INFO - ============================================================
2024-02-21 16:45:30,125 - __main__ - INFO - Environment: development
2024-02-21 16:45:30,125 - __main__ - INFO - Debug mode: True
2024-02-21 16:45:30,125 - __main__ - INFO - Host: 0.0.0.0
2024-02-21 16:45:30,125 - __main__ - INFO - Port: 5000
 * Serving Flask app 'app'
 * Debug mode: on
```

### Production Mode
```
2024-02-21 16:45:30,123 - __main__ - INFO - Running in PRODUCTION mode
2024-02-21 16:45:30,123 - __main__ - INFO - Logging level: WARNING
 * Serving Flask app 'app'
 * Debug mode: off
```

## Troubleshooting

### Database Connection Error
If you see database connection errors on startup, verify:
1. DATABASE_URL is correctly set in .env
2. Database server is accessible
3. SSL certificates are properly configured

### Configuration Error
If you see configuration validation errors:
1. Check that all required environment variables are set in .env
2. Verify JWT_SECRET_KEY is at least 32 characters
3. Ensure FLASK_PORT is between 1 and 65535

### Import Errors
If you see import errors:
1. Ensure you're running from the project root directory
2. Verify virtual environment is activated
3. Check that all dependencies are installed: `pip install -r requirements.txt`
