# Render Deployment Guide

This guide will help you deploy your AI Quiz Generator application on Render.

## Prerequisites

1. A Render account (sign up at [render.com](https://render.com))
2. Your project pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Environment variables ready (see below)

## Project Structure

Render will deploy:
- **Backend**: FastAPI application as a Web Service
- **Frontend**: Static site (optional, can be deployed separately)

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push your code to Git:**
   - Ensure all files are committed
   - Push to your repository

2. **Create a new Web Service on Render:**
   - Go to [render.com/dashboard](https://render.com/dashboard)
   - Click "New +" → "Blueprint"
   - Connect your Git repository
   - Render will detect `render.yaml` and create services automatically

3. **Set Environment Variables:**
   - Go to your Web Service → Environment
   - Add the following variables:
     - `DATABASE_URL` - PostgreSQL connection string
     - `GEMINI_API_KEY` - Your Google Gemini API key
     - `ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins

### Option 2: Manual Deployment

#### Backend Deployment:

1. **Create a new Web Service:**
   - Go to Render Dashboard → "New +" → "Web Service"
   - Connect your Git repository

2. **Configure the Service:**
   - **Name**: `quiz-generator-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: Leave as default (root of repo)

3. **Set Environment Variables:**
   - `DATABASE_URL` - PostgreSQL connection string
   - `GEMINI_API_KEY` - Your Google Gemini API key
   - `ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins

4. **Add PostgreSQL Database:**
   - Go to Render Dashboard → "New +" → "PostgreSQL"
   - Create a new PostgreSQL database
   - Copy the Internal Database URL
   - Set it as `DATABASE_URL` in your Web Service environment variables

#### Frontend Deployment:

1. **Create a new Static Site:**
   - Go to Render Dashboard → "New +" → "Static Site"
   - Connect your Git repository

2. **Configure the Static Site:**
   - **Name**: `quiz-generator-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
   - **Root Directory**: Leave as default

3. **Set Environment Variables:**
   - `VITE_API_BASE_URL` - Your backend API URL (e.g., `https://quiz-generator-api.onrender.com`)

## Environment Variables

### Required Variables:

1. **DATABASE_URL** - PostgreSQL connection string
   - Format: `postgresql://user:password@host:port/database`
   - Get this from your Render PostgreSQL database

2. **GEMINI_API_KEY** - Your Google Gemini API key
   - Get this from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Optional Variables:

- **ALLOWED_ORIGINS** - Comma-separated list of allowed CORS origins
  - Default: `http://localhost:5173`
  - For production: `https://your-frontend.onrender.com`

- **VITE_API_BASE_URL** - Frontend API base URL
  - Set this in the frontend Static Site environment variables
  - Example: `https://quiz-generator-api.onrender.com`

## Database Setup

### Using Render PostgreSQL:

1. **Create PostgreSQL Database:**
   - Go to Render Dashboard → "New +" → "PostgreSQL"
   - Choose a name and plan
   - Create the database

2. **Get Connection String:**
   - Go to your PostgreSQL database
   - Copy the "Internal Database URL"
   - Set it as `DATABASE_URL` in your Web Service

3. **Database Tables:**
   - Tables will be created automatically on first request
   - The app uses lazy initialization for database tables

## API Endpoints

After deployment, your API will be available at:
- `https://your-service.onrender.com/health` - Health check
- `https://your-service.onrender.com/test-db` - Database test
- `https://your-service.onrender.com/generate_quiz` - Generate quiz
- `https://your-service.onrender.com/history` - Get quiz history
- `https://your-service.onrender.com/quiz/{id}` - Get specific quiz

## Frontend Configuration

Update `frontend/src/services/api.js` to use your Render backend URL:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (import.meta.env.PROD ? 'https://your-backend.onrender.com' : 'http://localhost:8000');
```

Or set `VITE_API_BASE_URL` in your Render Static Site environment variables.

## Troubleshooting

### Backend Not Starting

- Check the build logs in Render Dashboard
- Verify all dependencies are in `backend/requirements.txt`
- Check that the start command is correct

### Database Connection Issues

- Verify `DATABASE_URL` is set correctly
- Use the "Internal Database URL" from Render PostgreSQL
- Check that the database is in the same region as your service

### CORS Issues

- Set `ALLOWED_ORIGINS` to include your frontend URL
- Check that CORS middleware is configured correctly

### Frontend Not Loading

- Verify build command completed successfully
- Check that `frontend/dist` directory exists
- Verify `VITE_API_BASE_URL` is set correctly

## Post-Deployment

1. **Test the API:**
   - Visit `https://your-service.onrender.com/health`
   - Test database connection: `https://your-service.onrender.com/test-db`

2. **Update Frontend:**
   - Set `VITE_API_BASE_URL` to your backend URL
   - Redeploy the frontend

3. **Monitor Logs:**
   - Check Render Dashboard → Logs for any errors
   - Monitor database connections

## Support

For issues specific to:
- **Render**: Check [Render Documentation](https://render.com/docs)
- **FastAPI**: Check [FastAPI Documentation](https://fastapi.tiangolo.com)
- **React/Vite**: Check [Vite Documentation](https://vitejs.dev)

