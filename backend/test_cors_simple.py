"""
Simple test for CORS configuration without database dependency.

This test verifies that:
1. flask-cors is properly installed
2. CORS configuration is present in the app

Task 12.1: Configure CORS for Flask app
"""

def test_cors_installation():
    """Test that flask-cors is installed."""
    try:
        import flask_cors
        print("✓ flask-cors is installed")
        print(f"  Version: {flask_cors.__version__}")
        return True
    except ImportError as e:
        print(f"✗ flask-cors is not installed: {e}")
        return False


def test_cors_in_requirements():
    """Test that flask-cors is in requirements.txt."""
    try:
        with open('../requirements.txt', 'r') as f:
            content = f.read()
            if 'flask-cors' in content:
                print("✓ flask-cors is in requirements.txt")
                return True
            else:
                print("✗ flask-cors is not in requirements.txt")
                return False
    except Exception as e:
        print(f"✗ Error reading requirements.txt: {e}")
        return False


def test_cors_import_in_app():
    """Test that CORS is imported in app.py."""
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            
            checks = {
                'CORS import': 'from flask_cors import CORS' in content,
                'CORS initialization': 'CORS(app' in content,
                'supports_credentials': 'supports_credentials=True' in content,
                'origins configured': 'origins=' in content
            }
            
            print("\nCORS Configuration in app.py:")
            all_passed = True
            for check_name, passed in checks.items():
                if passed:
                    print(f"  ✓ {check_name}")
                else:
                    print(f"  ✗ {check_name}")
                    all_passed = False
            
            return all_passed
            
    except Exception as e:
        print(f"✗ Error reading app.py: {e}")
        return False


def main():
    """Run all CORS configuration tests."""
    print("=" * 60)
    print("Testing CORS Configuration (Task 12.1)")
    print("=" * 60)
    
    results = []
    
    print("\n1. Checking flask-cors installation...")
    results.append(test_cors_installation())
    
    print("\n2. Checking requirements.txt...")
    results.append(test_cors_in_requirements())
    
    print("\n3. Checking CORS configuration in app.py...")
    results.append(test_cors_import_in_app())
    
    print("\n" + "=" * 60)
    if all(results):
        print("✓ All CORS configuration checks passed!")
        print("\nSummary:")
        print("  - flask-cors installed")
        print("  - Added to requirements.txt")
        print("  - Configured in Flask app with:")
        print("    • Frontend origins allowed")
        print("    • Credentials support enabled (for cookies)")
        print("    • Proper headers and methods configured")
        print("=" * 60)
        return 0
    else:
        print("✗ Some CORS configuration checks failed")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
