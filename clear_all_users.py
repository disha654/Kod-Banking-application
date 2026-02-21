"""
Script to delete ALL users from the database.
WARNING: This will permanently delete all user accounts and their data!
"""
import sys
sys.path.insert(0, 'backend')

from db import execute_query, initialize_connection_pool

# Initialize database connection
print("Connecting to database...")
initialize_connection_pool()
print("✓ Connected to database\n")

def clear_all_users():
    """Delete all users from the database."""
    try:
        # First, show current users
        query = "SELECT COUNT(*) as count FROM users"
        result = execute_query(query, fetch=True)
        
        if result and len(result) > 0:
            user_count = result[0]['count']
            print(f"\n⚠️  Found {user_count} users in the database")
        else:
            print("Could not count users")
            return False
        
        if user_count == 0:
            print("✓ Database is already empty")
            return True
        
        # Confirm deletion
        print("\n⚠️  WARNING: This will permanently delete ALL users!")
        confirm = input("Type 'DELETE ALL' to confirm: ").strip()
        
        if confirm != 'DELETE ALL':
            print("❌ Cancelled. No users were deleted.")
            return False
        
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

def list_users():
    """List all users in the database."""
    try:
        query = "SELECT uid, username, email, phone, balance FROM users"
        result = execute_query(query, fetch=True)
        
        if result and len(result) > 0:
            print("\n=== Current Users ===")
            print(f"{'UID':<10} {'Username':<20} {'Email':<30} {'Phone':<15} {'Balance':<10}")
            print("-" * 90)
            for user in result:
                print(f"{user['uid']:<10} {user['username']:<20} {user['email']:<30} {user['phone']:<15} {user['balance']:<10.2f}")
            print(f"\nTotal users: {len(result)}")
        else:
            print("\n✓ No users in database")
            
    except Exception as e:
        print(f"❌ Error listing users: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 60)
    print("  KODBANK - DELETE ALL USERS")
    print("=" * 60)
    
    # List all users first
    list_users()
    
    # Clear all users
    clear_all_users()
    
    # Show final state
    print("\n" + "=" * 60)
    print("  FINAL STATE")
    print("=" * 60)
    list_users()
