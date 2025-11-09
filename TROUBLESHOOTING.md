# Troubleshooting Vercel Deployment

## Common Issues and Solutions

### Issue: Python process exited with exit status 1

This error typically occurs during the build or initialization phase. Here are the most common causes and solutions:

#### 1. Missing Dependencies

**Symptom:** Import errors in logs

**Solution:**
- Ensure `api/requirements.txt` includes all dependencies from `backend/requirements.txt`
- Make sure `mangum` is included (required for FastAPI on Vercel)
- Check that all Python packages are compatible with Vercel's Python runtime

#### 2. Database Connection Issues

**Symptom:** Database initialization errors

**Solution:**
- Set `DATABASE_URL` environment variable in Vercel dashboard
- For production, use PostgreSQL (not SQLite)
- Ensure database allows connections from Vercel IPs
- The app now uses lazy initialization, so DB errors won't crash startup

#### 3. Import Path Issues

**Symptom:** ModuleNotFoundError or ImportError

**Solution:**
- The API wrapper (`api/index.py`) should automatically handle path resolution
- Check Vercel build logs for the debug output showing paths
- Ensure `backend/` directory is included in your repository

#### 4. Missing Environment Variables

**Symptom:** API key errors or configuration errors

**Required Variables:**
- `GEMINI_API_KEY` - Your Google Gemini API key
- `DATABASE_URL` - Database connection string

**How to Set:**
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add each variable for Production, Preview, and Development
3. Redeploy after adding variables

#### 5. CORS Issues

**Symptom:** Frontend can't connect to API

**Solution:**
- CORS is automatically configured for Vercel deployments
- If issues persist, check that `VERCEL` environment variable is set (automatically set by Vercel)

## Debugging Steps

### 1. Check Build Logs

In Vercel Dashboard:
1. Go to your project
2. Click on the failed deployment
3. Check the "Build Logs" tab
4. Look for Python errors or import errors

### 2. Check Function Logs

1. Go to Vercel Dashboard → Your Project → Functions
2. Click on the API function
3. Check runtime logs for errors

### 3. Test Locally

Test the API wrapper locally:
```bash
cd api
python index.py
```

### 4. Verify File Structure

Ensure your repository has this structure:
```
.
├── api/
│   ├── index.py
│   └── requirements.txt
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── scraper.py
│   ├── llm_quiz_generator.py
│   └── requirements.txt
├── frontend/
│   └── ...
└── vercel.json
```

## Recent Fixes Applied

1. **Lazy Database Initialization**: Database now initializes on first request, not at startup
2. **Better Error Handling**: Added try-catch blocks to prevent startup failures
3. **Debug Logging**: Added detailed logging in API wrapper to help identify issues
4. **Path Resolution**: Improved path handling for imports

## Next Steps if Error Persists

1. **Check the specific error message** in Vercel build logs
2. **Verify environment variables** are set correctly
3. **Check that all files are committed** to your repository
4. **Review the debug output** in the API wrapper logs

If you see specific error messages, share them and we can provide targeted fixes.

