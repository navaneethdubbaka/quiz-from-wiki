"""
Vercel serverless function wrapper for FastAPI backend
"""
import sys
import os
import traceback

# Get the directory where this file is located (api/)
api_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root (parent of api/)
project_root = os.path.dirname(api_dir)

# Try multiple possible backend locations:
# 1. Backend copied into api/backend (during build)
# 2. Backend in project root (original location)
backend_paths = [
    os.path.join(api_dir, 'backend'),  # Copied during build
    os.path.join(project_root, 'backend'),  # Original location
]

# Find the first existing backend path
backend_path = None
for path in backend_paths:
    if os.path.exists(path):
        backend_path = path
        break

# Debug: Print paths for troubleshooting
print(f"API wrapper: api_dir = {api_dir}")
print(f"API wrapper: project_root = {project_root}")
print(f"API wrapper: backend_path = {backend_path}")
print(f"API wrapper: backend_path exists = {os.path.exists(backend_path)}")
print(f"API wrapper: Current working directory = {os.getcwd()}")

# Add multiple possible paths to sys.path
paths_to_add = []
if backend_path:
    paths_to_add.append(backend_path)
paths_to_add.extend([
    project_root,  # Project root (in case imports are relative to root)
    os.path.join(project_root, '..'),  # Parent of project root
])

for path in paths_to_add:
    if path and os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)
        print(f"API wrapper: Added to sys.path: {path}")

print(f"API wrapper: sys.path (first 5): {sys.path[:5]}")

# Try to list files in backend directory for debugging
if os.path.exists(backend_path):
    try:
        backend_files = os.listdir(backend_path)
        print(f"API wrapper: Backend directory files: {backend_files[:10]}")
    except Exception as e:
        print(f"API wrapper: Could not list backend files: {e}")

# Set working directory to backend for relative imports
original_cwd = os.getcwd()
try:
    if os.path.exists(backend_path):
        os.chdir(backend_path)
        print(f"API wrapper: Changed working directory to {os.getcwd()}")
except Exception as e:
    print(f"API wrapper: Warning - Could not change directory: {e}")

# Import the FastAPI app after setting up paths
try:
    print("API wrapper: Attempting to import from main...")
    # Try importing based on where backend is located
    if backend_path and os.path.exists(backend_path):
        # If backend is in api/backend (copied during build)
        if backend_path == os.path.join(api_dir, 'backend'):
            try:
                from backend.main import app
                print("API wrapper: Successfully imported app from backend.main (copied location)")
            except ImportError:
                # Fallback to direct import
                from main import app
                print("API wrapper: Successfully imported app from main (direct)")
        else:
            # Backend is in original location
            from main import app
            print("API wrapper: Successfully imported app from main (original location)")
    else:
        # No backend found, try direct import
        from main import app
        print("API wrapper: Successfully imported app from main (fallback)")
except Exception as e:
    # Print detailed error for debugging
    print(f"API wrapper: Import error: {e}")
    print(f"API wrapper: Error type: {type(e).__name__}")
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

