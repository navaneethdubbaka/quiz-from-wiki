"""
Vercel serverless function wrapper for FastAPI backend
"""
import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Change to backend directory to ensure relative imports work
os.chdir(backend_path)

# Import the FastAPI app
from main import app

# Use Mangum to wrap FastAPI for AWS Lambda/Vercel
from mangum import Mangum

# Export the handler for Vercel
handler = Mangum(app, lifespan="off")

