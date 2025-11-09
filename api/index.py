"""
Vercel serverless function wrapper for FastAPI backend
"""
import sys
import os
import traceback

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
backend_path = os.path.abspath(backend_path)

# Debug: Print paths for troubleshooting
print(f"API wrapper: backend_path = {backend_path}")
print(f"API wrapper: backend_path exists = {os.path.exists(backend_path)}")
print(f"API wrapper: sys.path = {sys.path[:3]}")

# Add to Python path
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Set working directory to backend for relative imports
original_cwd = os.getcwd()
try:
    if os.path.exists(backend_path):
        os.chdir(backend_path)
        print(f"API wrapper: Changed working directory to {backend_path}")
except Exception as e:
    print(f"API wrapper: Warning - Could not change directory: {e}")

# Import the FastAPI app after setting up paths
try:
    print("API wrapper: Attempting to import from main...")
    from main import app
    print("API wrapper: Successfully imported app")
except Exception as e:
    # Print detailed error for debugging
    print(f"API wrapper: Import error: {e}")
    print(f"API wrapper: Traceback:")
    traceback.print_exc()
    # Restore cwd and re-raise
    try:
        os.chdir(original_cwd)
    except:
        pass
    raise

# Use Mangum to wrap FastAPI for AWS Lambda/Vercel
try:
    from mangum import Mangum
    print("API wrapper: Successfully imported Mangum")
except Exception as e:
    print(f"API wrapper: Mangum import error: {e}")
    traceback.print_exc()
    raise

# Export the handler for Vercel
# lifespan="off" disables startup/shutdown events which can cause issues in serverless
try:
    handler = Mangum(app, lifespan="off")
    print("API wrapper: Successfully created Mangum handler")
except Exception as e:
    print(f"API wrapper: Handler creation error: {e}")
    traceback.print_exc()
    raise

