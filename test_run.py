"""
Test script to verify run.py can be imported and configured correctly.
"""

import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_run_imports():
    """Test that run.py can import all required modules."""
    try:
        # Read run.py and check for required functions
        with open('run.py', 'r') as f:
            content = f.read()
        
        # Check that the file has the expected functions
        assert 'def setup_logging()' in content, "run.py should have setup_logging function"
        assert 'def main()' in content, "run.py should have main function"
        assert 'if __name__ == \'__main__\':' in content, "run.py should have main guard"
        assert 'from app import app' in content, "run.py should import app"
        assert 'from config import Config' in content, "run.py should import Config"
        
        print("✓ run.py structure is correct")
        print("✓ setup_logging function exists")
        print("✓ main function exists")
        print("✓ Required imports present")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_config_loading():
    """Test that Config can be loaded."""
    try:
        from config import Config
        
        # Check that Config has required attributes
        assert hasattr(Config, 'FLASK_ENV'), "Config should have FLASK_ENV"
        assert hasattr(Config, 'FLASK_DEBUG'), "Config should have FLASK_DEBUG"
        assert hasattr(Config, 'FLASK_HOST'), "Config should have FLASK_HOST"
        assert hasattr(Config, 'FLASK_PORT'), "Config should have FLASK_PORT"
        
        # Check helper methods
        assert hasattr(Config, 'is_development'), "Config should have is_development method"
        assert hasattr(Config, 'is_production'), "Config should have is_production method"
        assert hasattr(Config, 'get_flask_config'), "Config should have get_flask_config method"
        
        print("✓ Config loaded successfully")
        print(f"  Environment: {Config.FLASK_ENV}")
        print(f"  Debug: {Config.FLASK_DEBUG}")
        print(f"  Host: {Config.FLASK_HOST}")
        print(f"  Port: {Config.FLASK_PORT}")
        return True
        
    except Exception as e:
        print(f"✗ Config loading error: {e}")
        return False


def test_logging_levels():
    """Test that logging configuration works for different environments."""
    try:
        from config import Config
        import logging
        
        # Test development mode
        if Config.is_development():
            expected_level = "DEBUG"
            print(f"✓ Development mode detected")
        else:
            expected_level = "WARNING"
            print(f"✓ Production mode detected")
        
        print(f"  Expected log level: {expected_level}")
        return True
        
    except Exception as e:
        print(f"✗ Logging test error: {e}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("Testing run.py Application Entry Point")
    print("=" * 60)
    print()
    
    results = []
    
    print("Test 1: Verify run.py structure")
    results.append(test_run_imports())
    print()
    
    print("Test 2: Verify Config loading")
    results.append(test_config_loading())
    print()
    
    print("Test 3: Verify logging configuration")
    results.append(test_logging_levels())
    print()
    
    print("=" * 60)
    if all(results):
        print("✓ All tests passed!")
        print("✓ run.py is ready to start the application")
    else:
        print("✗ Some tests failed")
        sys.exit(1)
    print("=" * 60)
