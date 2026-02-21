"""
Script to delete ALL users from the database WITHOUT confirmation.
WARNING: This will permanently delete all user accounts and their data!
"""
import sys
sys.path.insert(0, 'backend')

from db import execute_query, initialize_connection_pool

# Initialize database connection
print("Connecting to database...")
initialize_connection_pool()
print("✓ Connected to database\n")

def clear_all_users_now():
    """Delete all users from the database without confirmation."""
    try:
        # First, show current users
        query = "SELECT COUNT(*) as count FROM users"
        result = execute_query(query, fetch=True)
        
        if result and len(result) > 0:
            user_count = result[0]['count']
            print(f"⚠️  Found {user_count} users in the database")
        else:
            print("✓ Database is already empty")
            return True
        
        if user_count == 0:
            print("✓ Database is already empty")
            return True
        
        # Delete all transactions first (foreign key constraint)
        print("\n🗑️  Deleting all transactions...")
        query = "DELETE FROM transactions"
        rows_affected = execute_query(query, fetch=False)
        print(f"✓ Deleted {rows_affected} transactions")
        
        # Delete all JWT tokens
        print("🗑️  Deleting all JWT tokens...")
        query = "DELETE FROM cjwt"
        rows_affected = execute_query(query, fetch=False)
        print(f"✓ Deleted {rows_affected} JWT tokens")
        
        # Delete all users
        print("🗑️  Deleting all users...")
        query = "DELETE FROM users"
        rows_affected = execute_query(query, fetch=False)
        print(f"✅ Successfully deleted {rows_affected} users")
        print("✅ Database cleared successfully!")
        return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("  KODBANK - DELETE ALL USERS (NO CONFIRMATION)")
    print("=" * 60)
    
    # Clear all users
    clear_all_users_now()
    
    # Verify deletion
    print("\n" + "=" * 60)
    print("  VERIFICATION")
    print("=" * 60)
    
    query = "SELECT COUNT(*) as count FROM users"
    result = execute_query(query, fetch=True)
    if result and len(result) > 0:
        user_count = result[0]['count']
        print(f"✓ Users remaining: {user_count}")
    
    query = "SELECT COUNT(*) as count FROM cjwt"
    result = execute_query(query, fetch=True)
    if result and len(result) > 0:
        token_count = result[0]['count']
        print(f"✓ JWT tokens remaining: {token_count}")
    
    query = "SELECT COUNT(*) as count FROM transactions"
    result = execute_query(query, fetch=True)
    if result and len(result) > 0:
        transaction_count = result[0]['count']
        print(f"✓ Transactions remaining: {transaction_count}")
