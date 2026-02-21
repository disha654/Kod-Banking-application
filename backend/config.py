"""
Configuration module for kodbank1 application.

This module loads and validates environment variables, providing
centralized configuration management for the application.

Requirements: 4.1, 5.1
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Exception raised for configuration errors."""
    pass


class Config:
    """
    Application configuration class.
    
    Loads configuration from environment variables and validates
    that all required settings are present.
    """
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRY_HOURS = int(os.getenv('JWT_EXPIRY_HOURS', '1'))
    
    # Application Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5500,http://127.0.0.1:5500,http://127.0.0.1:3000').split(',')
    
    # Security Configuration
    COOKIE_SECURE = os.getenv('COOKIE_SECURE', 'True').lower() == 'true'
    COOKIE_HTTPONLY = True
    COOKIE_SAMESITE = 'Strict'
    
    @classmethod
    def validate(cls):
        """
        Validate that all required configuration variables are set.
        
        Raises:
            ConfigurationError: If any required configuration is missing or invalid
        """
        errors = []
        
        # Validate DATABASE_URL
        if not cls.DATABASE_URL:
            errors.append("DATABASE_URL environment variable is required")
        elif not cls.DATABASE_URL.startswith('mysql://'):
            errors.append("DATABASE_URL must start with 'mysql://'")
        
        # Validate JWT_SECRET_KEY
        if not cls.JWT_SECRET_KEY:
            errors.append("JWT_SECRET_KEY environment variable is required")
        elif len(cls.JWT_SECRET_KEY) < 32:
            errors.append("JWT_SECRET_KEY must be at least 32 characters long for security")
        
        # Validate JWT_EXPIRY_HOURS
        if cls.JWT_EXPIRY_HOURS <= 0:
            errors.append("JWT_EXPIRY_HOURS must be a positive integer")
        
        # Validate FLASK_PORT
        if not (1 <= cls.FLASK_PORT <= 65535):
            errors.append("FLASK_PORT must be between 1 and 65535")
        
        # If there are validation errors, raise exception
        if errors:
            error_message = "Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            logger.error(error_message)
            raise ConfigurationError(error_message)
        
        logger.info("Configuration validation successful")
    
    @classmethod
    def get_database_config(cls):
        """
        Get database configuration dictionary.
        
        Returns:
            dict: Database configuration with URL
        """
        return {
            'url': cls.DATABASE_URL
        }
    
    @classmethod
    def get_jwt_config(cls):
        """
        Get JWT configuration dictionary.
        
        Returns:
            dict: JWT configuration with secret key, algorithm, and expiry
        """
        return {
            'secret_key': cls.JWT_SECRET_KEY,
            'algorithm': cls.JWT_ALGORITHM,
            'expiry_hours': cls.JWT_EXPIRY_HOURS
        }
    
    @classmethod
    def get_flask_config(cls):
        """
        Get Flask application configuration dictionary.
        
        Returns:
            dict: Flask configuration with environment, debug, host, and port
        """
        return {
            'env': cls.FLASK_ENV,
            'debug': cls.FLASK_DEBUG,
            'host': cls.FLASK_HOST,
            'port': cls.FLASK_PORT
        }
    
    @classmethod
    def get_cors_config(cls):
        """
        Get CORS configuration dictionary.
        
        Returns:
            dict: CORS configuration with allowed origins
        """
        return {
            'origins': cls.CORS_ORIGINS,
            'supports_credentials': True
        }
    
    @classmethod
    def get_cookie_config(cls):
        """
        Get cookie configuration dictionary.
        
        Returns:
            dict: Cookie configuration with security settings
        """
        return {
            'secure': cls.COOKIE_SECURE,
            'httponly': cls.COOKIE_HTTPONLY,
            'samesite': cls.COOKIE_SAMESITE,
            'max_age': cls.JWT_EXPIRY_HOURS * 3600  # Convert hours to seconds
        }
    
    @classmethod
    def is_production(cls):
        """
        Check if application is running in production mode.
        
        Returns:
            bool: True if FLASK_ENV is 'production', False otherwise
        """
        return cls.FLASK_ENV == 'production'
    
    @classmethod
    def is_development(cls):
        """
        Check if application is running in development mode.
        
        Returns:
            bool: True if FLASK_ENV is 'development', False otherwise
        """
        return cls.FLASK_ENV == 'development'


# Validate configuration on module import
# Skip validation if SKIP_CONFIG_VALIDATION is set (for testing)
if not os.getenv('SKIP_CONFIG_VALIDATION'):
    try:
        Config.validate()
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        # Re-raise to prevent application from starting with invalid configuration
        raise
else:
    logger.warning("Configuration validation skipped (SKIP_CONFIG_VALIDATION=1)")
