"""
Simple test script to verify database connection.
Run this to ensure the database connection module works correctly.
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from db import initialize_connection_pool, get_connection, close_connection_pool

def test_connection():
    """Test database connection and basic operations."""
    print("Testing database connection...")
    
    try:
        # Initialize connection pool
        print("1. Initializing connection pool...")
        initialize_connection_pool()
        print("   ✓ Connection pool initialized successfully")
        
        # Get a connection
        print("2. Getting connection from pool...")
        conn = get_connection()
        print("   ✓ Connection obtained successfully")
        
        # Test a simple query
        print("3. Testing simple query...")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print(f"   ✓ Query executed successfully: {result}")
        
        # Cleanup
        print("4. Cleaning up...")
        close_connection_pool()
        print("   ✓ Connection pool closed")
        
        print("\n✅ All tests passed! Database connection is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
