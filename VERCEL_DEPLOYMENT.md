# Vercel Deployment Guide

This guide will help you deploy your AI Quiz Generator application on Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Your project pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Environment variables ready (see below)

## Environment Variables

You need to set the following environment variables in Vercel:

### Required Variables

1. **GEMINI_API_KEY** - Your Google Gemini API key for quiz generation
2. **DATABASE_URL** - Database connection string
   - For SQLite: `sqlite:///./quiz_generator.db`
   - For PostgreSQL (recommended for production): `postgresql://user:password@host:port/database`
   - You can use Vercel Postgres or an external database service

### Optional Variables

- **ALLOWED_ORIGINS** - Comma-separated list of allowed CORS origins (defaults to localhost for dev)
- **VITE_API_BASE_URL** - Frontend API base URL (usually not needed, auto-detects `/api` in production)

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Import your project:**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "Add New" → "Project"
   - Import your Git repository

2. **Configure the project:**
   - Framework Preset: **Other** (or leave as auto-detected)
   - Root Directory: Leave as default (root of repo)
   - Build Command: `cd frontend && npm run build`
   - Output Directory: `frontend/dist`
   - Install Command: `cd frontend && npm install`

3. **Add Environment Variables:**
   - Go to Project Settings → Environment Variables
   - Add all required variables listed above
   - Make sure to add them for Production, Preview, and Development

4. **Deploy:**
   - Click "Deploy"
   - Wait for the build to complete

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Set Environment Variables:**
   ```bash
   vercel env add GEMINI_API_KEY
   vercel env add DATABASE_URL
   ```

5. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

## Project Structure

The deployment is configured as follows:

- **Frontend**: Static site built from `frontend/` directory
- **Backend API**: Serverless functions in `api/` directory
- **Routes**: 
  - `/api/*` → Backend API endpoints
  - `/*` → Frontend React app

## API Routes

After deployment, your API will be available at:
- `https://your-project.vercel.app/api/generate_quiz`
- `https://your-project.vercel.app/api/history`
- `https://your-project.vercel.app/api/quiz/{id}`

## Database Setup

### Option 1: Vercel Postgres (Recommended)

1. Go to your Vercel project dashboard
2. Navigate to Storage → Create Database
3. Select Postgres
4. Copy the connection string and set it as `DATABASE_URL`

### Option 2: External Database

Use any PostgreSQL database service (e.g., Supabase, Neon, Railway) and set the connection string as `DATABASE_URL`.

### Option 3: SQLite (Not Recommended for Production)

For development/testing only, you can use SQLite:
```
DATABASE_URL=sqlite:///./quiz_generator.db
```

**Note:** SQLite files are ephemeral on Vercel serverless functions and will be lost between deployments. Use PostgreSQL for production.

## Troubleshooting

### Build Fails

- Check that all dependencies are in `package.json`
- Ensure Python dependencies are in `api/requirements.txt`
- Check build logs in Vercel dashboard

### API Not Working

- Verify environment variables are set correctly
- Check that CORS is configured properly
- Review function logs in Vercel dashboard

### Database Connection Issues

- Verify `DATABASE_URL` is set correctly
- Ensure database allows connections from Vercel IPs
- Check database credentials

## Post-Deployment

1. Update your frontend API URL if needed (should auto-detect `/api`)
2. Test all API endpoints
3. Monitor function logs for any errors
4. Set up custom domain (optional) in Vercel project settings

## Support

For issues specific to:
- **Vercel**: Check [Vercel Documentation](https://vercel.com/docs)
- **FastAPI**: Check [FastAPI Documentation](https://fastapi.tiangolo.com)
- **React/Vite**: Check [Vite Documentation](https://vitejs.dev)

