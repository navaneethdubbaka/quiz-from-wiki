# Render Manual Deployment Setup

If you're deploying manually (not using Blueprint), use these settings in the Render Dashboard:

## Backend Web Service Configuration

### Basic Settings:
- **Name**: `quiz-generator-api`
- **Environment**: `Python 3`
- **Region**: Choose your preferred region
- **Branch**: `main` (or your default branch)

### Build & Deploy:
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Environment Variables:
Add these in the "Environment" section:
- `DATABASE_URL` - PostgreSQL connection string (from your Render PostgreSQL database)
- `GEMINI_API_KEY` - Your Google Gemini API key
- `ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins (e.g., `https://your-frontend.onrender.com`)

### Health Check:
- **Health Check Path**: `/health`

## Frontend Static Site Configuration

### Basic Settings:
- **Name**: `quiz-generator-frontend`
- **Environment**: `Static Site`
- **Branch**: `main` (or your default branch)

### Build & Deploy:
- **Root Directory**: Leave empty (root of repo)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish Directory**: `frontend/dist`

### Environment Variables:
- `VITE_API_BASE_URL` - Your backend URL (e.g., `https://quiz-generator-api.onrender.com`)

## Important Notes:

1. **Root Directory is critical** - Set it to `backend` for the backend service
2. **Start Command must use $PORT** - Render sets this automatically
3. **Build Command** - Must reference `requirements.txt` from the backend directory
4. **Environment Variables** - Must be set in the Render Dashboard

## Quick Setup Steps:

1. **Delete existing service** (if it's not working)
2. **Create new Web Service** → Connect your Git repo
3. **Set Root Directory**: `backend`
4. **Set Build Command**: `pip install -r requirements.txt`
5. **Set Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. **Add Environment Variables**
7. **Deploy**

## Alternative: Use Blueprint (Recommended)

Instead of manual setup, use Blueprint deployment:

1. Go to Render Dashboard → "New +" → "Blueprint"
2. Connect your Git repository
3. Render will automatically detect `render.yaml` and create services
4. Set environment variables
5. Deploy

This is easier and uses the `render.yaml` configuration automatically.

