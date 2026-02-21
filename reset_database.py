"""
Script to completely reset the database - drops all tables and recreates them.
WARNING: This will permanently delete ALL data!
"""
import sys
sys.path.insert(0, 'backend')

from db import execute_query, initialize_connection_pool

# Initialize database connection
print("Connecting to database...")
initialize_connection_pool()
print("✓ Connected to database\n")

def reset_database():
    """Drop all tables and recreate them."""
    try:
        print("=" * 60)
        print("  RESETTING DATABASE")
        print("=" * 60)
        
        # Confirm
        print("\n⚠️  WARNING: This will delete ALL data in the database!")
        confirm = input("Type 'RESET' to confirm: ").strip()
        
        if confirm != 'RESET':
            print("❌ Cancelled.")
            return False
        
        # Disable foreign key checks
        print("\n🔧 Disabling foreign key checks...")
        try:
            execute_query("SET FOREIGN_KEY_CHECKS = 0", fetch=False)
        except:
            pass
        
        # Drop tables in correct order
        tables = ['transactions', 'cjwt', 'kodusers', 'users']
        
        for table in tables:
            print(f"🗑️  Dropping table: {table}")
            try:
                result = execute_query(f"DROP TABLE IF EXISTS {table}", fetch=False)
                print(f"   ✓ Dropped {table}")
            except Exception as e:
                print(f"   ⚠️  Could not drop {table}: {e}")
        
        # Re-enable foreign key checks
        print("\n🔧 Re-enabling foreign key checks...")
        try:
            execute_query("SET FOREIGN_KEY_CHECKS = 1", fetch=False)
        except:
            pass
        
        # Create tables
        print("\n📝 Creating tables...")
        
        # Create users table
        create_users = """
        CREATE TABLE IF NOT EXISTS users (
            uid VARCHAR(50) PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20) NOT NULL,
            balance DECIMAL(15, 2) DEFAULT 0.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_username (username),
            INDEX idx_email (email)
        )
        """
        result = execute_query(create_users, fetch=False)
        try:
            if result and result.get('success'):
                print("   ✓ Created users table")
            else:
                print(f"   ✓ Created users table")
        except:
            print("   ✓ Created users table")
        
        # Create transactions table
        create_transactions = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender_username VARCHAR(50) NOT NULL,
            receiver_username VARCHAR(50) NOT NULL,
            amount DECIMAL(15, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_username) REFERENCES users(username) ON DELETE CASCADE,
            FOREIGN KEY (receiver_username) REFERENCES users(username) ON DELETE CASCADE,
            INDEX idx_sender (sender_username),
            INDEX idx_receiver (receiver_username),
            INDEX idx_created_at (created_at)
        )
        """
        result = execute_query(create_transactions, fetch=False)
        try:
            if result and result.get('success'):
                print("   ✓ Created transactions table")
            else:
                print("   ✓ Created transactions table")
        except:
            print("   ✓ Created transactions table")
        
        # Create cjwt table
        create_cjwt = """
        CREATE TABLE IF NOT EXISTS cjwt (
            id INT AUTO_INCREMENT PRIMARY KEY,
            token TEXT NOT NULL,
            uid VARCHAR(50) NOT NULL,
            expiry TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (uid) REFERENCES users(uid) ON DELETE CASCADE,
            INDEX idx_uid (uid),
            INDEX idx_expiry (expiry)
        )
        """
        result = execute_query(create_cjwt, fetch=False)
        try:
            if result and result.get('success'):
                print("   ✓ Created cjwt table")
            else:
                print("   ✓ Created cjwt table")
        except:
            print("   ✓ Created cjwt table")
        
        print("\n✅ Database reset successfully!")
        print("✅ All tables created!")
        print("\n📊 You can now register new users.")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == '__main__':
    reset_database()
