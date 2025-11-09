# Frontend Deployment on Render

## Quick Setup Steps

### 1. Create Static Site on Render

1. **Go to Render Dashboard:**
   - Click "New +" → "Static Site"
   - Connect your Git repository

2. **Configure the Static Site:**
   - **Name**: `quiz-generator-frontend` (or any name you prefer)
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (root of repo)
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`

3. **Set Environment Variable:**
   - Go to "Environment" tab
   - Add: `VITE_API_BASE_URL` = `https://your-backend-service.onrender.com`
     - Replace `your-backend-service` with your actual backend service name
     - Example: If your backend is `quiz-generator-api.onrender.com`, use that

4. **Deploy:**
   - Click "Create Static Site"
   - Render will build and deploy your frontend

## Important Notes

### Environment Variable:
- **`VITE_API_BASE_URL`** must be set to your backend URL
- Format: `https://your-backend-service.onrender.com`
- No trailing slash needed
- This tells the frontend where to find the API

### CORS Configuration:
Make sure your backend has the frontend URL in `ALLOWED_ORIGINS`:
- Go to your backend service → Environment
- Set `ALLOWED_ORIGINS` to: `https://your-frontend-service.onrender.com`
- Or use comma-separated list: `https://frontend1.onrender.com,https://frontend2.onrender.com`

## After Deployment

1. **Get your frontend URL:**
   - Render will provide a URL like: `https://quiz-generator-frontend.onrender.com`

2. **Update backend CORS:**
   - Go to backend service → Environment
   - Update `ALLOWED_ORIGINS` to include your frontend URL

3. **Test the connection:**
   - Visit your frontend URL
   - Try generating a quiz
   - Check browser console for any CORS errors

## Troubleshooting

### Frontend can't connect to backend:
- Check that `VITE_API_BASE_URL` is set correctly
- Verify backend URL is accessible (visit `/health` endpoint)
- Check browser console for errors

### CORS errors:
- Make sure `ALLOWED_ORIGINS` in backend includes your frontend URL
- Check that backend CORS middleware is configured correctly

### Build fails:
- Check that `frontend/package.json` exists
- Verify all dependencies are listed
- Check build logs for specific errors

