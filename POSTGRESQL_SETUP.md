# PostgreSQL Setup for Vercel

## Setting Up PostgreSQL on Vercel

### Option 1: Vercel Postgres (Recommended)

1. **Create Vercel Postgres Database:**
   - Go to your Vercel project dashboard
   - Navigate to **Storage** → **Create Database**
   - Select **Postgres**
   - Choose a name for your database
   - Click **Create**

2. **Get Connection String:**
   - After creating the database, Vercel automatically sets environment variables:
     - `POSTGRES_URL` - Connection string with connection pooling
     - `POSTGRES_PRISMA_URL` - Prisma-compatible connection string
     - `POSTGRES_URL_NON_POOLING` - Direct connection (no pooling)

3. **Environment Variables:**
   - The code automatically detects Vercel Postgres environment variables
   - No need to manually set `DATABASE_URL` if using Vercel Postgres
   - The code will use `POSTGRES_URL` if available

### Option 2: External PostgreSQL Database

If using an external PostgreSQL service (Supabase, Neon, Railway, etc.):

1. **Get Connection String:**
   - Format: `postgresql://user:password@host:port/database`
   - Example: `postgresql://user:pass@db.example.com:5432/mydb`

2. **Set Environment Variable:**
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add `DATABASE_URL` with your PostgreSQL connection string
   - Make sure to add it for Production, Preview, and Development

## Testing PostgreSQL Connection

### 1. Test via API Endpoint

After deploying, test the database connection:

```bash
# Test database connection
curl https://your-domain.vercel.app/api/test-db
```

Expected response:
```json
{
  "status": "success",
  "database_type": "PostgreSQL",
  "connection": "ok",
  "tables_created": true,
  "quiz_count": 0,
  "timestamp": "2025-01-09T..."
}
```

### 2. Test via Health Endpoint

```bash
# Basic health check
curl https://your-domain.vercel.app/api/health
```

### 3. Test Database Operations

Try creating a quiz to test database write operations:

```bash
curl -X POST https://your-domain.vercel.app/api/generate_quiz \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Python_(programming_language)"}'
```

## Troubleshooting

### Issue: Connection Refused

**Symptom:** `test-db` endpoint returns connection error

**Solutions:**
- Verify `DATABASE_URL` or `POSTGRES_URL` is set correctly
- Check that database allows connections from Vercel IPs
- For external databases, ensure firewall rules allow Vercel IPs
- Verify database credentials are correct

### Issue: Tables Not Created

**Symptom:** `test-db` returns `"tables_created": false`

**Solutions:**
- The tables will be created automatically on first use
- Or call `/api/generate_quiz` which will initialize the database
- Check function logs for any initialization errors

### Issue: Connection Pool Exhausted

**Symptom:** Database connection errors under load

**Solutions:**
- The code uses a small connection pool (pool_size=1) for serverless
- This is normal for serverless functions
- Connections are recycled automatically

## Database Schema

The application creates the following table:

```sql
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    url VARCHAR(500) NOT NULL UNIQUE,
    title VARCHAR(300) NOT NULL,
    date_generated TIMESTAMP NOT NULL,
    scraped_content TEXT,
    full_quiz_data TEXT NOT NULL
);
```

## Environment Variables Summary

| Variable | Description | Required |
|----------|-------------|----------|
| `POSTGRES_URL` | Vercel Postgres connection string | Auto-set by Vercel |
| `DATABASE_URL` | External PostgreSQL connection string | If not using Vercel Postgres |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

## Next Steps

1. **Set up PostgreSQL** (Vercel Postgres or external)
2. **Deploy your application**
3. **Test the connection** using `/api/test-db`
4. **Verify tables are created** by checking the response
5. **Test full functionality** by generating a quiz

