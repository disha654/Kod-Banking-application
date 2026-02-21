#!/usr/bin/env python3
"""
Database schema initialization script for kodbank1 application.

This script reads the schema.sql file and executes the SQL statements
to create the required database tables (kodusers and CJWT) with indexes.

Usage:
    python init_db.py
"""

import os
import sys
import logging
from pathlib import Path
from db import initialize_connection_pool, get_connection, is_pool_initialized
from mysql.connector import Error

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def read_schema_file(schema_path='backend/schema.sql'):
    """
    Read the SQL schema file.
    
    Args:
        schema_path (str): Path to the schema.sql file
        
    Returns:
        str: Contents of the schema file
        
    Raises:
        FileNotFoundError: If schema file doesn't exist
    """
    # Try multiple possible paths
    possible_paths = [
        schema_path,
        'schema.sql',
        os.path.join(os.path.dirname(__file__), 'schema.sql')
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            logger.info(f"Reading schema from: {path}")
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    
    raise FileNotFoundError(
        f"Schema file not found. Tried paths: {', '.join(possible_paths)}"
    )


def execute_schema(schema_sql):
    """
    Execute the schema SQL statements.
    
    Args:
        schema_sql (str): SQL statements to execute
        
    Returns:
        bool: True if successful, False otherwise
    """
    connection = None
    cursor = None
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Split the schema into individual statements
        # Remove comments and empty lines
        statements = []
        current_statement = []
        
        for line in schema_sql.split('\n'):
            # Skip comment lines
            stripped = line.strip()
            if stripped.startswith('--') or not stripped:
                continue
            
            current_statement.append(line)
            
            # Check if statement is complete (ends with semicolon)
            if stripped.endswith(';'):
                statement = '\n'.join(current_statement)
                statements.append(statement)
                current_statement = []
        
        # Execute each statement
        logger.info(f"Executing {len(statements)} SQL statements...")
        
        for i, statement in enumerate(statements, 1):
            try:
                logger.debug(f"Executing statement {i}/{len(statements)}")
                cursor.execute(statement)
                connection.commit()
                logger.info(f"Statement {i}/{len(statements)} executed successfully")
            except Error as e:
                logger.error(f"Error executing statement {i}: {e}")
                logger.error(f"Statement: {statement[:100]}...")
                connection.rollback()
                raise
        
        logger.info("Schema initialization completed successfully")
        return True
        
    except Error as e:
        logger.error(f"Database error during schema initialization: {e}")
        if connection:
            connection.rollback()
        return False
    except Exception as e:
        logger.error(f"Unexpected error during schema initialization: {e}")
        if connection:
            connection.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def main():
    """
    Main function to initialize the database schema.
    """
    logger.info("Starting database schema initialization...")
    
    try:
        # Initialize connection pool if not already initialized
        if not is_pool_initialized():
            logger.info("Initializing database connection pool...")
            initialize_connection_pool()
        
        # Read schema file
        logger.info("Reading schema file...")
        schema_sql = read_schema_file()
        
        # Execute schema
        logger.info("Executing schema statements...")
        success = execute_schema(schema_sql)
        
        if success:
            logger.info("=" * 60)
            logger.info("Database schema initialized successfully!")
            logger.info("Tables created: kodusers, CJWT")
            logger.info("Indexes created: username, email, uid, expiry")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Schema initialization failed")
            return 1
            
    except FileNotFoundError as e:
        logger.error(f"Schema file error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
