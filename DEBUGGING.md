# Debugging the 500 Error

## Current Issue
The function is crashing with a 500 error. This means:
- ✅ Routing is working (function is being invoked)
- ❌ Function is crashing during execution

## Most Likely Causes:

1. **Backend directory not found** - The backend directory might not be included in the deployment
2. **Import errors** - Backend modules might not be importing correctly
3. **Database connection error** - DATABASE_URL might not be set or invalid
4. **Missing dependencies** - Some Python packages might be missing

## How to Debug:

### 1. Check Function Logs in Vercel Dashboard:
1. Go to Vercel Dashboard → Your Project
2. Click on "Functions" tab
3. Click on `api/index.py`
4. Check the "Runtime Logs"
5. Look for messages starting with "API wrapper:"

### 2. What to Look For:
- `API wrapper: backend_path = ...` - Shows if backend directory is found
- `API wrapper: backend_path exists = ...` - Shows if directory exists
- `API wrapper: Import error: ...` - Shows any import errors
- `API wrapper: Backend directory files: ...` - Shows what files are found

### 3. Common Issues:

#### Issue: Backend directory not found
**Symptom:** `API wrapper: backend_path exists = False`
**Solution:** 
- Check that `backend/` directory is committed to Git
- Verify `includeFiles` in `vercel.json` is correct
- Check that backend files are in the repository

#### Issue: Import errors
**Symptom:** `API wrapper: Import error: ...`
**Solution:**
- Check that all backend Python files are present
- Verify all dependencies are in `api/requirements.txt`
- Check for circular imports or missing modules

#### Issue: Database connection error
**Symptom:** Database initialization warnings
**Solution:**
- Set `DATABASE_URL` environment variable in Vercel
- Use PostgreSQL for production (not SQLite)
- Verify database credentials are correct

## Next Steps:

1. **Check the Function Logs** - This will show exactly where it's failing
2. **Share the logs** - Copy the "API wrapper:" messages from the logs
3. **Fix the specific issue** - Based on what the logs show

The debug output should pinpoint exactly where the function is crashing.

