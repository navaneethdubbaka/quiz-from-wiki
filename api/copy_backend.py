"""
Build script to copy backend files into api directory for Vercel deployment
This ensures the backend code is accessible to the serverless function
"""
import os
import shutil
import sys

def copy_backend_files():
    """Copy backend Python files to api directory"""
    # Get paths
    api_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(api_dir)
    backend_dir = os.path.join(project_root, 'backend')
    api_backend_dir = os.path.join(api_dir, 'backend')
    
    print(f"Copying backend files from {backend_dir} to {api_backend_dir}")
    
    if not os.path.exists(backend_dir):
        print(f"ERROR: Backend directory not found: {backend_dir}")
        sys.exit(1)
    
    # Create backend directory in api if it doesn't exist
    if os.path.exists(api_backend_dir):
        shutil.rmtree(api_backend_dir)
    
    # Copy backend directory
    shutil.copytree(backend_dir, api_backend_dir, ignore=shutil.ignore_patterns(
        '__pycache__',
        '*.pyc',
        'venv',
        'sample_outputs',
        '*.db',
        '*.sqlite3'
    ))
    
    print(f"✅ Backend files copied successfully to {api_backend_dir}")

if __name__ == "__main__":
    copy_backend_files()

