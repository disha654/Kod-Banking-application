"""
Test CORS configuration for Flask app.

This test verifies that:
1. flask-cors is properly installed
2. CORS is configured to allow frontend origins
3. Credentials support is enabled for cookie-based authentication

Task 12.1: Configure CORS for Flask app
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_cors_import():
    """Test that flask-cors can be imported."""
    try:
        from flask_cors import CORS
        print("✓ flask-cors imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import flask-cors: {e}")
        return False


def test_cors_configuration():
    """Test that CORS is configured in the Flask app."""
    try:
        from app import app
        
        # Check if CORS extension is registered
        # CORS adds specific headers to responses
        with app.test_client() as client:
            # Make an OPTIONS request (preflight) from an allowed origin
            response = client.options(
                '/api/register',
                headers={'Origin': 'http://localhost:3000'}
            )
            
            # Check for CORS headers
            cors_headers = {
                'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials'),
                'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
            }
            
            print("\nCORS Headers in Response:")
            for header, value in cors_headers.items():
                if value:
                    print(f"  ✓ {header}: {value}")
                else:
                    print(f"  ✗ {header}: Not set")
            
            # Verify credentials support
            if cors_headers['Access-Control-Allow-Credentials'] == 'true':
                print("\n✓ Credentials support enabled (supports_credentials=True)")
            else:
                print("\n✗ Credentials support not enabled")
                return False
            
            # Verify origin is allowed
            if cors_headers['Access-Control-Allow-Origin'] == 'http://localhost:3000':
                print("✓ Frontend origin allowed")
            else:
                print("✗ Frontend origin not properly configured")
                return False
            
            return True
            
    except Exception as e:
        print(f"✗ Error testing CORS configuration: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all CORS configuration tests."""
    print("=" * 60)
    print("Testing CORS Configuration (Task 12.1)")
    print("=" * 60)
    
    results = []
    
    print("\n1. Testing flask-cors installation...")
    results.append(test_cors_import())
    
    print("\n2. Testing CORS configuration in Flask app...")
    results.append(test_cors_configuration())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All CORS configuration tests passed!")
        print("=" * 60)
        return 0
    else:
        print("✗ Some CORS configuration tests failed")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
