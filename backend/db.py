"""
Database connection module for kodbank1 application.

This module provides connection pool management for AIVEN MySQL database
with SSL support and error handling.
"""

import os
import logging
from urllib.parse import urlparse, parse_qs
import mysql.connector
from mysql.connector import pooling, Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database connection pool
_connection_pool = None


def parse_database_url(url):
    """
    Parse the DATABASE_URL into connection parameters.
    
    Args:
        url (str): Database URL in format mysql://user:pass@host:port/db?ssl-mode=REQUIRED
        
    Returns:
        dict: Dictionary containing connection parameters
        
    Raises:
        ValueError: If URL format is invalid
    """
    try:
        parsed = urlparse(url)
        
        if parsed.scheme != 'mysql':
            raise ValueError(f"Invalid database scheme: {parsed.scheme}. Expected 'mysql'")
        
        # Parse query parameters
        query_params = parse_qs(parsed.query)
        ssl_mode = query_params.get('ssl-mode', [''])[0]
        
        config = {
            'host': parsed.hostname,
            'port': int(parsed.port) if parsed.port else 3306,
            'user': parsed.username,
            'password': parsed.password,
            'database': parsed.path.lstrip('/'),
        }
        
        # Configure SSL if required
        if ssl_mode == 'REQUIRED':
            config['ssl_disabled'] = False
            # For AIVEN, we need to allow self-signed certificates
            config['ssl_verify_cert'] = False
            config['ssl_verify_identity'] = False
        
        return config
    except Exception as e:
        logger.error(f"Failed to parse DATABASE_URL: {e}")
        raise ValueError(f"Invalid DATABASE_URL format: {e}")


def initialize_connection_pool():
    """
    Initialize the database connection pool.
    
    This function should be called once during application startup.
    It creates a connection pool with SSL configuration as required.
    
    Raises:
        SystemExit: If connection pool initialization fails
    """
    global _connection_pool
    
    if _connection_pool is not None:
        logger.warning("Connection pool already initialized")
        return
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL environment variable not set")
        raise SystemExit("DATABASE_URL environment variable is required")
    
    try:
        # Parse connection parameters
        db_config = parse_database_url(database_url)
        
        logger.info(f"Initializing connection pool for {db_config['host']}:{db_config['port']}")
        
        # Create connection pool
        _connection_pool = pooling.MySQLConnectionPool(
            pool_name="kodbank_pool",
            pool_size=5,
            pool_reset_session=True,
            **db_config
        )
        
        # Test the connection
        test_connection = _connection_pool.get_connection()
        test_connection.close()
        
        logger.info("Database connection pool initialized successfully")
        
    except Error as e:
        logger.error(f"Database connection error: {e}")
        logger.error("Failed to initialize database connection pool")
        raise SystemExit(f"Database connection failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during connection pool initialization: {e}")
        raise SystemExit(f"Failed to initialize database: {e}")


def get_connection():
    """
    Get a connection from the pool.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection
        
    Raises:
        Error: If unable to get connection from pool
    """
    global _connection_pool
    
    if _connection_pool is None:
        logger.error("Connection pool not initialized. Call initialize_connection_pool() first")
        raise Error("Database connection pool not initialized")
    
    try:
        connection = _connection_pool.get_connection()
        return connection
    except Error as e:
        logger.error(f"Failed to get connection from pool: {e}")
        raise


def is_pool_initialized():
    """
    Check if the connection pool is initialized.
    
    Returns:
        bool: True if pool is initialized, False otherwise
    """
    return _connection_pool is not None


def test_connection():
    """
    Test the database connection by executing a simple query.
    
    Returns:
        bool: True if connection test succeeds, False otherwise
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False


def close_connection_pool():
    """
    Close all connections in the pool.
    
    This should be called during application shutdown.
    """
    global _connection_pool
    
    if _connection_pool is None:
        return
    
    try:
        # Connection pool doesn't have a direct close method
        # Connections are closed when they're returned to the pool
        logger.info("Connection pool cleanup completed")
        _connection_pool = None
    except Exception as e:
        logger.error(f"Error during connection pool cleanup: {e}")


def execute_query(query, params=None, fetch=False):
    """
    Execute a database query with error handling.
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters for prepared statements
        fetch (bool): Whether to fetch results (for SELECT queries)
        
    Returns:
        list or int: Query results if fetch=True, otherwise affected row count
        
    Raises:
        Error: If query execution fails
    """
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(query, params or ())
        
        if fetch:
            results = cursor.fetchall()
            return results
        else:
            connection.commit()
            return cursor.rowcount
            
    except Error as e:
        if connection:
            connection.rollback()
        logger.error(f"Query execution error: {e}")
        logger.error(f"Query: {query}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
