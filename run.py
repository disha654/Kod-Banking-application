"""
Application entry point for kodbank1 banking system.

This module starts the Flask application with appropriate configuration
for development or production mode, including logging setup.

Requirements: 4.5
"""

import sys
import os
import logging

# Add backend directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import app
from config import Config

# Configure logging based on environment
def setup_logging():
    """
    Configure logging for the application based on environment.
    
    Development mode: INFO level with detailed format
    Production mode: WARNING level with structured format
    """
    log_level = logging.DEBUG if Config.is_development() else logging.WARNING
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('kodbank1.log')
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    if Config.is_production():
        logger.info("Running in PRODUCTION mode")
        logger.info("Logging level: WARNING")
    else:
        logger.info("Running in DEVELOPMENT mode")
        logger.info("Logging level: DEBUG")
    
    return logger


def main():
    """
    Main entry point for the application.
    
    Sets up logging, validates configuration, and starts the Flask server.
    """
    try:
        # Setup logging
        logger = setup_logging()
        
        # Log application startup
        logger.info("=" * 60)
        logger.info("Starting kodbank1 Banking Application")
        logger.info("=" * 60)
        
        # Get Flask configuration
        flask_config = Config.get_flask_config()
        
        # Log configuration details
        logger.info(f"Environment: {flask_config['env']}")
        logger.info(f"Debug mode: {flask_config['debug']}")
        logger.info(f"Host: {flask_config['host']}")
        logger.info(f"Port: {flask_config['port']}")
        
        # Start Flask application
        app.run(
            host=flask_config['host'],
            port=flask_config['port'],
            debug=flask_config['debug']
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
