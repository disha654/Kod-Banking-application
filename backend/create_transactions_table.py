"""
Script to add transactions table to existing database.
"""
import os
import sys
import logging

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from db import get_connection, initialize_connection_pool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_transactions_table():
    """Create transactions table in the database."""
    try:
        logger.info("Initializing database connection pool...")
        initialize_connection_pool()
        
        logger.info("Reading SQL file...")
        sql_file = os.path.join(os.path.dirname(__file__), 'add_transactions_table.sql')
        
        with open(sql_file, 'r') as f:
            sql_content = f.read()
        
        logger.info("Creating transactions table...")
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql_content)
        connection.commit()
        
        cursor.close()
        connection.close()
        
        logger.info("✓ Transactions table created successfully!")
        
    except Exception as e:
        logger.error(f"Failed to create transactions table: {e}")
        raise

if __name__ == '__main__':
    create_transactions_table()
