# Deployment Guide for Render

This guide will help you deploy the AIVideoResponder application on Render with separate frontend and backend services.

## Prerequisites

1. GitHub account with your code repository
2. Render account (free tier available)

## Backend Deployment

### Step 1: Create Web Service

1. Log into your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:

**Basic Settings:**
- **Name**: `aivideo-backend` (or your preferred name)
- **Root Directory**: `backend`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

**Advanced Settings:**
- **Auto-Deploy**: Yes (recommended)

### Step 2: Environment Variables

No additional environment variables are required for basic functionality. Render automatically sets the `PORT` variable.

### Step 3: Deploy

Click "Create Web Service" and wait for the deployment to complete. Note the service URL (e.g., `https://aivideo-backend-xxx.onrender.com`).

## Frontend Deployment

### Step 1: Create Static Site

1. In Render dashboard, click "New +" and select "Static Site"
2. Connect your GitHub repository
3. Configure the site:

**Basic Settings:**
- **Name**: `aivideo-frontend` (or your preferred name)
- **Root Directory**: `frontend`
- **Branch**: `main` (or your default branch)

**Build Settings:**
- **Build Command**: `npm install && npm run build`
- **Publish Directory**: `dist`

### Step 2: Environment Variables

Add the following environment variable:
- **Key**: `VITE_API_URL`
- **Value**: Your backend service URL (e.g., `https://aivideo-backend-xxx.onrender.com`)

### Step 3: Deploy

Click "Create Static Site" and wait for the deployment to complete.

## Post-Deployment Configuration

### Update Frontend Environment

After both services are deployed, update the frontend environment variable:

1. Go to your frontend service in Render
2. Navigate to "Environment" tab
3. Update `VITE_API_URL` with your actual backend URL
4. The site will automatically redeploy

### Test the Application

1. Visit your frontend URL
2. Test the audio recording functionality
3. Verify the backend API is responding correctly

## Troubleshooting

### Backend Issues

**Build Failures:**
- Check that all dependencies in `requirements.txt` are valid
- Ensure Python version compatibility (3.9.16 recommended)

**Runtime Errors:**
- Check the service logs in Render dashboard
- Verify all required files are in the `backend` directory
- Ensure model files (`.pkl`) are included in the repository

### Frontend Issues

**Build Failures:**
- Verify `package.json` is valid
- Check Node.js version compatibility (18+ recommended)

**API Connection Issues:**
- Verify `VITE_API_URL` is set correctly
- Check CORS configuration in backend
- Ensure backend service is running

### Performance Optimization

**Backend:**
- Consider upgrading to a paid plan for better performance
- Implement caching for model predictions
- Optimize video generation process

**Frontend:**
- Enable gzip compression (automatic on Render)
- Optimize bundle size with code splitting
- Use CDN for static assets

## Monitoring

### Health Checks

Both services include health check endpoints:
- Backend: `GET /` returns service status
- Frontend: Automatic health checks via Render

### Logs

Access logs through the Render dashboard:
1. Select your service
2. Go to "Logs" tab
3. Monitor real-time logs and errors

## Scaling

### Free Tier Limitations

- Services may sleep after 15 minutes of inactivity
- Limited CPU and memory resources
- 750 hours per month across all services

### Upgrading

Consider upgrading to paid plans for:
- Always-on services (no sleeping)
- Better performance and resources
- Custom domains
- Priority support

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to the repository
2. **CORS**: Configure appropriate CORS settings for production
3. **File Uploads**: Implement file size and type validation
4. **Rate Limiting**: Consider implementing rate limiting for API endpoints

## Maintenance

### Updates

1. Push changes to your GitHub repository
2. Services will automatically redeploy (if auto-deploy is enabled)
3. Monitor deployment logs for any issues

### Backup

- Model files and datasets are stored in the repository
- Database files are included in the backend deployment
- Consider external storage for user-generated content

## Support

For deployment issues:
1. Check Render documentation: https://render.com/docs
2. Review service logs in the dashboard
3. Contact Render support for platform-specific issues