# Database Setup for Render

## Issue
The backend is trying to connect to `localhost` instead of your Render PostgreSQL database. This means `DATABASE_URL` is not set correctly.

## Solution

### Step 1: Create PostgreSQL Database in Render

1. Go to **Render Dashboard** → **New +** → **PostgreSQL**
2. Fill in the details:
   - **Name**: `quiz-generator-db` (or any name you prefer)
   - **Database**: `quiz_generator_db` (or leave default)
   - **User**: Leave default (auto-generated)
   - **Region**: Choose same region as your backend service
   - **PostgreSQL Version**: Latest (recommended)
   - **Plan**: Free tier is fine for development
3. Click **Create Database**

### Step 2: Get Connection String

1. After the database is created, click on it
2. Go to **Connections** tab
3. Copy the **Internal Database URL** (for services in same region) or **External Database URL** (for external access)
4. The URL looks like:
   ```
   postgresql://user:password@hostname:5432/database_name
   ```

### Step 3: Set DATABASE_URL in Backend Service

1. Go to your **Backend Web Service** (quiz-generator-api)
2. Go to **Environment** tab
3. Add or update the `DATABASE_URL` variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the connection string from Step 2
4. Click **Save Changes**

### Step 4: Redeploy

1. After setting `DATABASE_URL`, Render will automatically redeploy
2. Or manually trigger a redeploy from the **Manual Deploy** tab

## Verify Database Connection

After redeploying, check the logs:

1. Go to your backend service → **Logs**
2. Look for:
   - `📊 Database: PostgreSQL - ...` (should show PostgreSQL, not SQLite)
   - `✅ Database engine created: PostgreSQL`
   - `✅ Database tables created successfully!`

If you see SQLite or localhost errors, the `DATABASE_URL` is not set correctly.

## Test Database Connection

You can test the database connection using the `/test-db` endpoint:

```bash
curl https://your-backend.onrender.com/test-db
```

Expected response:
```json
{
  "status": "success",
  "database_type": "PostgreSQL",
  "connection": "ok",
  "tables_created": true,
  "quiz_count": 0,
  "timestamp": "..."
}
```

## Troubleshooting

### Still seeing localhost errors?

1. **Check environment variable is set**:
   - Go to backend service → Environment
   - Verify `DATABASE_URL` exists and has the correct value
   - Make sure there are no extra spaces or quotes

2. **Check database is running**:
   - Go to PostgreSQL service → Status should be "Available"

3. **Check connection string format**:
   - Should start with `postgresql://` or `postgresql+psycopg2://`
   - Should include username, password, host, port, and database name

4. **Check region**:
   - Backend and database should be in the same region for best performance
   - Use Internal Database URL if in same region

### Connection timeout errors?

- Make sure you're using the **Internal Database URL** if backend and database are in the same region
- If using External URL, ensure your database allows external connections

## Quick Checklist

- [ ] PostgreSQL database created in Render
- [ ] Connection string copied from database service
- [ ] `DATABASE_URL` environment variable set in backend service
- [ ] Backend service redeployed
- [ ] Logs show PostgreSQL connection (not SQLite)
- [ ] `/test-db` endpoint returns success

