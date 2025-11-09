# Quick Fix: Database Connection Error

## The Problem
You're seeing this error:
```
connection to server at "localhost" (::1), port 5432 failed: Connection refused
```

This means `DATABASE_URL` is **not set** or **set incorrectly** in Render.

## Quick Solution (5 minutes)

### Step 1: Create PostgreSQL Database in Render

1. Go to **Render Dashboard**: https://dashboard.render.com
2. Click **New +** → **PostgreSQL**
3. Fill in:
   - **Name**: `quiz-generator-db` (or any name)
   - **Database**: Leave default
   - **Region**: Same as your backend service
   - **Plan**: Free (for development)
4. Click **Create Database**
5. Wait for it to be created (takes ~1 minute)

### Step 2: Get Connection String

1. Click on your new database
2. Go to **Connections** tab
3. Find **Internal Database URL** (use this if backend and database are in same region)
4. Copy the entire URL - it looks like:
   ```
   postgresql://user:password@hostname:5432/database_name
   ```

### Step 3: Set DATABASE_URL in Backend Service

1. Go to your **Backend Web Service** (quiz-generator-api)
2. Click on **Environment** tab (left sidebar)
3. Find `DATABASE_URL` in the list, or click **Add Environment Variable**
4. Set:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the connection string from Step 2
5. Click **Save Changes**

### Step 4: Redeploy

1. Render will automatically redeploy after saving
2. Or go to **Manual Deploy** tab → **Deploy latest commit**

### Step 5: Check Logs

1. Go to **Logs** tab
2. Look for these messages:
   - ✅ `🔍 DATABASE_URL from environment: SET`
   - ✅ `📊 Database: PostgreSQL - ...`
   - ✅ `✅ Database engine created: PostgreSQL`
   - ✅ `✅ Database connection test successful`

If you see these, the database is connected! ✅

## Troubleshooting

### Still seeing localhost errors?

1. **Check DATABASE_URL is set**:
   - Go to backend service → Environment
   - Verify `DATABASE_URL` exists
   - Make sure it starts with `postgresql://` (not `postgres://` or `localhost`)

2. **Check the connection string format**:
   - Should be: `postgresql://user:password@host:port/database`
   - Should NOT be: `postgresql://localhost` or `localhost:5432`

3. **Check database is running**:
   - Go to database service → Status should be "Available"

4. **Check logs after redeploy**:
   - Look for `🔍 DATABASE_URL from environment: SET` or `NOT SET`
   - If it says `NOT SET`, the environment variable wasn't saved correctly

### Common Mistakes

❌ **Wrong**: `DATABASE_URL=localhost:5432`  
✅ **Correct**: `DATABASE_URL=postgresql://user:password@host:5432/dbname`

❌ **Wrong**: `DATABASE_URL=postgres://...` (missing 'ql')  
✅ **Correct**: `DATABASE_URL=postgresql://...`

❌ **Wrong**: Using External URL when backend and database are in same region  
✅ **Correct**: Use Internal Database URL for same region

## Still Need Help?

Check the logs - the new logging will show:
- Whether DATABASE_URL is set
- What value it has (password masked)
- Whether connection test passed or failed

This will tell you exactly what's wrong!

