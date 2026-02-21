# Database Connection Module

## Overview

The `db.py` module provides connection pool management for the kodbank1 application's AIVEN MySQL database with SSL support and comprehensive error handling.

## Features

- **Connection Pooling**: Efficient connection management with a pool of 5 connections
- **SSL Support**: Automatic SSL configuration when `ssl-mode=REQUIRED` is in the connection string
- **Error Handling**: Comprehensive error logging and graceful failure handling
- **URL Parsing**: Automatic parsing of MySQL connection URLs from environment variables
- **Query Helper**: Convenient `execute_query()` function for common database operations

## Requirements Met

This module satisfies the following requirements from the kodbank1 specification:

- **Requirement 4.1**: Establishes connection to AIVEN MySQL database using provided connection URL
- **Requirement 4.2**: Uses SSL mode as required by the connection string
- **Requirement 4.5**: Logs errors and prevents application startup on connection failure

## Usage

### 1. Initialize Connection Pool (Application Startup)

```python
from backend.db import initialize_connection_pool

# Call this once during application startup
initialize_connection_pool()
```

This will:
- Load the `DATABASE_URL` from environment variables
- Parse the connection parameters including SSL settings
- Create a connection pool with 5 connections
- Test the connection to ensure it works
- Exit the application if connection fails

### 2. Get a Connection

```python
from backend.db import get_connection

# Get a connection from the pool
conn = get_connection()

# Use the connection
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM kodusers WHERE username = %s", (username,))
results = cursor.fetchall()

# Always close cursor and connection when done
cursor.close()
conn.close()
```

### 3. Execute Queries (Helper Function)

```python
from backend.db import execute_query

# SELECT query (fetch=True)
users = execute_query(
    "SELECT * FROM kodusers WHERE email = %s",
    params=(email,),
    fetch=True
)

# INSERT/UPDATE/DELETE query (fetch=False)
rows_affected = execute_query(
    "INSERT INTO kodusers (uid, username, email, password, balance, phone) VALUES (%s, %s, %s, %s, %s, %s)",
    params=(uid, username, email, hashed_password, 1000002, phone),
    fetch=False
)
```

### 4. Cleanup (Application Shutdown)

```python
from backend.db import close_connection_pool

# Call this during application shutdown
close_connection_pool()
```

## Environment Variables

The module requires the following environment variable:

```
DATABASE_URL=mysql://user:password@host:port/database?ssl-mode=REQUIRED
```

Example:
```
DATABASE_URL=mysql://avnadmin:mypassword@mysql-kodbank-project.aivencloud.com:12345/defaultdb?ssl-mode=REQUIRED
```

## SSL Configuration

When `ssl-mode=REQUIRED` is present in the connection URL, the module automatically configures:
- `ssl_disabled = False`
- `ssl_verify_cert = True`
- `ssl_verify_identity = True`

This ensures secure connections to the AIVEN MySQL database.

## Error Handling

The module provides comprehensive error handling:

1. **Missing DATABASE_URL**: Logs error and exits with SystemExit
2. **Invalid URL Format**: Raises ValueError with details
3. **Connection Failure**: Logs error and exits with SystemExit
4. **Query Errors**: Logs error, rolls back transaction, and raises Error
5. **Pool Not Initialized**: Raises Error when trying to get connection

All errors are logged with appropriate severity levels (INFO, WARNING, ERROR).

## Logging

The module uses Python's standard logging module with the following format:

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

Example log output:
```
2024-01-15 10:30:45,123 - db - INFO - Initializing connection pool for mysql-kodbank-project.aivencloud.com:12345
2024-01-15 10:30:45,456 - db - INFO - Database connection pool initialized successfully
```

## Testing

A test script is provided to verify the database connection:

```bash
python backend/test_db_connection.py
```

This will:
1. Initialize the connection pool
2. Get a connection from the pool
3. Execute a simple test query
4. Clean up resources
5. Report success or failure

## Connection Pool Configuration

The connection pool is configured with:
- **Pool Name**: `kodbank_pool`
- **Pool Size**: 5 connections
- **Pool Reset Session**: True (resets session variables between uses)

These settings provide a good balance between performance and resource usage for the kodbank1 application.

## Security Considerations

- Database credentials are loaded from environment variables (never hardcoded)
- SSL/TLS encryption is enforced when required by the connection string
- Prepared statements are supported via parameterized queries
- Connection pool prevents connection exhaustion attacks
- Errors are logged without exposing sensitive credentials

## Dependencies

- `mysql-connector-python==8.2.0`
- `python-dotenv==1.0.0`

## Notes

- The connection pool must be initialized before any database operations
- Always close connections after use to return them to the pool
- The `execute_query()` helper automatically handles connection lifecycle
- Transactions are automatically rolled back on errors
- The module is thread-safe (connection pool handles concurrent access)
