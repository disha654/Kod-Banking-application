"""
Demonstration script for the configuration module.

This script shows how to use the Config class to access
application configuration values.
"""

from config import Config

def main():
    """Demonstrate configuration module usage."""
    
    print("=" * 60)
    print("kodbank1 Configuration Module Demo")
    print("=" * 60)
    print()
    
    # Validate configuration
    print("1. Validating configuration...")
    try:
        Config.validate()
        print("   ✓ Configuration is valid")
    except Exception as e:
        print(f"   ✗ Configuration error: {e}")
        return
    print()
    
    # Database configuration
    print("2. Database Configuration:")
    db_config = Config.get_database_config()
    print(f"   URL: {db_config['url'][:50]}...")
    print()
    
    # JWT configuration
    print("3. JWT Configuration:")
    jwt_config = Config.get_jwt_config()
    print(f"   Algorithm: {jwt_config['algorithm']}")
    print(f"   Expiry Hours: {jwt_config['expiry_hours']}")
    print(f"   Secret Key Length: {len(jwt_config['secret_key'])} characters")
    print()
    
    # Flask configuration
    print("4. Flask Configuration:")
    flask_config = Config.get_flask_config()
    print(f"   Environment: {flask_config['env']}")
    print(f"   Debug Mode: {flask_config['debug']}")
    print(f"   Host: {flask_config['host']}")
    print(f"   Port: {flask_config['port']}")
    print()
    
    # CORS configuration
    print("5. CORS Configuration:")
    cors_config = Config.get_cors_config()
    print(f"   Allowed Origins: {len(cors_config['origins'])} origins")
    for origin in cors_config['origins']:
        print(f"     - {origin}")
    print(f"   Supports Credentials: {cors_config['supports_credentials']}")
    print()
    
    # Cookie configuration
    print("6. Cookie Configuration:")
    cookie_config = Config.get_cookie_config()
    print(f"   Secure: {cookie_config['secure']}")
    print(f"   HttpOnly: {cookie_config['httponly']}")
    print(f"   SameSite: {cookie_config['samesite']}")
    print(f"   Max Age: {cookie_config['max_age']} seconds")
    print()
    
    # Environment checks
    print("7. Environment Checks:")
    print(f"   Is Production: {Config.is_production()}")
    print(f"   Is Development: {Config.is_development()}")
    print()
    
    print("=" * 60)
    print("Configuration module is working correctly!")
    print("=" * 60)


if __name__ == '__main__':
    main()
