"""
Vercel serverless function entry point for Kodbank Flask application.
"""
import sys
import os

# Add backend directory to Python path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import Flask app
from app import app

# Export the Flask app for Vercel
# Vercel will automatically handle WSGI
app = app
