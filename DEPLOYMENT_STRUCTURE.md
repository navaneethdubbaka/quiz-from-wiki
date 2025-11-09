# Deployment Structure Explanation

## How Backend is Deployed on Vercel

### Current Structure:
```
project-root/
├── api/
│   ├── index.py          # Serverless function wrapper
│   ├── requirements.txt  # Python dependencies
│   └── __init__.py       # Makes api a package
├── backend/
│   ├── main.py           # FastAPI app
│   ├── database.py       # Database setup
│   ├── models.py         # Pydantic models
│   ├── scraper.py        # Wikipedia scraper
│   └── llm_quiz_generator.py  # LLM integration
├── frontend/
│   └── ...               # React/Vite app
└── vercel.json           # Vercel configuration
```

### How It Works:

1. **Vercel includes all files** in your repository when deploying Python functions
2. **`api/index.py`** is the entry point for all `/api/*` routes
3. **`api/index.py`** uses Python path manipulation to import from the `backend/` directory
4. The backend code is accessed at runtime, not copied

### Path Resolution:

The `api/index.py` file:
1. Finds the project root directory
2. Locates the `backend/` directory
3. Adds it to `sys.path` so Python can import from it
4. Imports the FastAPI app from `backend/main.py`

### Why This Works:

- Vercel includes all files in the deployment package
- Python can access files in parent directories via `sys.path`
- The backend directory is accessible at runtime
- No need to copy files - they're already in the deployment

### If Backend Isn't Accessible:

If you're still getting errors, check:
1. **Is `backend/` committed to Git?** - Vercel only deploys committed files
2. **Check the debug logs** - The `api/index.py` will print paths to help debug
3. **Verify environment variables** - `DATABASE_URL` and `GEMINI_API_KEY` must be set

### Alternative Approach (if needed):

If the above doesn't work, you can:
1. Copy backend files into `api/backend/` during build
2. Use a build script to copy files
3. Restructure to have backend code directly in `api/`

But the current approach should work since Vercel includes all repository files.

