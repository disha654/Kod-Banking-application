-- Add transactions table for transaction history
-- This table stores all money transfers between users

CREATE TABLE IF NOT EXISTS transactions (
  id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Auto-increment transaction ID',
  sender_username VARCHAR(50) NOT NULL COMMENT 'Username of sender',
  receiver_username VARCHAR(50) NOT NULL COMMENT 'Username of receiver',
  amount DECIMAL(15, 2) NOT NULL COMMENT 'Transfer amount',
  transaction_type VARCHAR(20) NOT NULL DEFAULT 'transfer' COMMENT 'Type of transaction',
  status VARCHAR(20) NOT NULL DEFAULT 'completed' COMMENT 'Transaction status',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Transaction timestamp',
  INDEX idx_sender (sender_username),
  INDEX idx_receiver (receiver_username),
  INDEX idx_created_at (created_at),
  FOREIGN KEY (sender_username) REFERENCES kodusers(username) ON DELETE CASCADE,
  FOREIGN KEY (receiver_username) REFERENCES kodusers(username) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Transaction history for money transfers';
