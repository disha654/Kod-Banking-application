-- ============================================================================
-- Database schema for kodbank1 banking application
-- ============================================================================
-- 
-- This schema defines the database structure for the kodbank1 banking system.
-- It includes tables for:
-- 1. User account management (kodusers)
-- 2. JWT token storage and validation (CJWT)
--
-- Requirements: 4.3, 4.4
-- ============================================================================

-- Drop tables if they exist (for clean initialization)
-- Note: CJWT must be dropped first due to foreign key constraint
DROP TABLE IF EXISTS CJWT;
DROP TABLE IF EXISTS kodusers;

-- ============================================================================
-- Table: kodusers
-- ============================================================================
-- Stores user account information including credentials and balance.
--
-- Fields:
--   uid         - Unique user identifier (max 50 characters)
--   username    - Unique username for login (max 50 characters)
--   email       - Unique email address (max 100 characters)
--   password    - Bcrypt hashed password (255 characters for hash storage)
--   balance     - Account balance with 2 decimal precision (default: 100000.00)
--   phone       - Phone number (max 20 characters)
--   created_at  - Timestamp of account creation (auto-generated)
--
-- Indexes:
--   PRIMARY KEY on uid for fast lookups by user ID
--   UNIQUE INDEX on username for login validation
--   UNIQUE INDEX on email for duplicate prevention
--   INDEX on username for fast authentication queries
--   INDEX on email for duplicate checking
--
-- Security considerations:
--   - Password field stores bcrypt hash (never plaintext)
--   - UNIQUE constraints prevent duplicate accounts
--   - InnoDB engine provides ACID compliance
--   - utf8mb4 charset supports international characters
--
-- Requirements: 1.4, 4.3, 6.1
-- ============================================================================
CREATE TABLE kodusers (
  uid VARCHAR(50) PRIMARY KEY COMMENT 'Unique user identifier',
  username VARCHAR(50) UNIQUE NOT NULL COMMENT 'Unique username for login',
  email VARCHAR(100) UNIQUE NOT NULL COMMENT 'Unique email address',
  password VARCHAR(255) NOT NULL COMMENT 'Bcrypt hashed password',
  balance DECIMAL(15, 2) NOT NULL DEFAULT 1000002.00 COMMENT 'Account balance',
  phone VARCHAR(20) NOT NULL COMMENT 'Phone number',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation timestamp',
  INDEX idx_username (username),
  INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='User account information and credentials';

-- ============================================================================
-- Table: CJWT
-- ============================================================================
-- Stores JWT tokens for session management and validation.
--
-- Fields:
--   id          - Auto-increment primary key
--   token       - JWT token string (TEXT type for variable length)
--   uid         - User ID (foreign key to kodusers.uid)
--   expiry      - Token expiration timestamp
--   created_at  - Timestamp of token creation (auto-generated)
--
-- Indexes:
--   PRIMARY KEY on id for fast lookups
--   INDEX on uid for user-specific token queries
--   INDEX on expiry for expired token cleanup
--
-- Foreign Keys:
--   uid references kodusers(uid) with CASCADE delete
--   When a user is deleted, all their tokens are automatically deleted
--
-- Security considerations:
--   - Tokens are stored for server-side validation
--   - Expiry field enables token expiration enforcement
--   - CASCADE delete ensures orphaned tokens are removed
--   - InnoDB engine provides ACID compliance
--
-- Requirements: 2.4, 4.4, 5.1, 5.2
-- ============================================================================
CREATE TABLE CJWT (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Auto-increment primary key',
  token TEXT NOT NULL COMMENT 'JWT token string',
  uid VARCHAR(50) NOT NULL COMMENT 'User ID (foreign key)',
  expiry DATETIME NOT NULL COMMENT 'Token expiration timestamp',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Token creation timestamp',
  FOREIGN KEY (uid) REFERENCES kodusers(uid) ON DELETE CASCADE,
  INDEX idx_uid (uid),
  INDEX idx_expiry (expiry)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='JWT token storage for session management';
