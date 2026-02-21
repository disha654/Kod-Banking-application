"""
Vercel serverless function entry point for Kodbank Flask application.
"""
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app

# Vercel expects a handler function
def handler(request, context):
    return app(request.environ, context)
