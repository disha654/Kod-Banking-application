"""
Script to delete a user from the database.
Use this to clear existing users so you can re-register them.
"""
import sys
sys.path.insert(0, 'backend')

from db import execute_query

def delete_user(username):
    """Delete a user by username."""
    try:
        # Delete from users table
        query = "DELETE FROM users WHERE username = %s"
        result = execute_query(query, (username,), fetch=False)
        
        if result['success']:
            print(f"✓ Successfully deleted user: {username}")
            print(f"  Rows affected: {result.get('rows_affected', 0)}")
            return True
        else:
            print(f"✗ Failed to delete user: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def list_users():
    """List all users in the database."""
    try:
        query = "SELECT uid, username, email, phone, balance FROM users"
        result = execute_query(query, fetch=True)
        
        if result['success'] and result['data']:
            print("\n=== Current Users ===")
            print(f"{'UID':<10} {'Username':<20} {'Email':<30} {'Phone':<15} {'Balance':<10}")
            print("-" * 90)
            for user in result['data']:
                print(f"{user['uid']:<10} {user['username']:<20} {user['email']:<30} {user['phone']:<15} {user['balance']:<10.2f}")
            print(f"\nTotal users: {len(result['data'])}")
        else:
            print("No users found or error occurred")
            
    except Exception as e:
        print(f"✗ Error listing users: {e}")

if __name__ == '__main__':
    print("=== Kodbank User Management ===\n")
    
    # List all users first
    list_users()
    
    # Ask which user to delete
    print("\n")
    username = input("Enter username to delete (or press Enter to cancel): ").strip()
    
    if username:
        confirm = input(f"Are you sure you want to delete user '{username}'? (yes/no): ").strip().lower()
        if confirm == 'yes':
            delete_user(username)
            print("\n")
            list_users()
        else:
            print("Cancelled.")
    else:
        print("Cancelled.")
