# EventEase AI Bot - DigitalOcean App Platform Deployment Guide

This guide will help you deploy the EventEase AI Bot to DigitalOcean App Platform.

## Prerequisites

1. **DigitalOcean Account**: Create an account at [DigitalOcean](https://digitalocean.com)
2. **GitHub Repository**: Ensure your code is pushed to a GitHub repository
3. **Gradient AI API Key**: Get your API key from [Gradient AI](https://gradient.ai)

## Project Structure

Your project consists of:

- **Backend**: FastAPI application (`/app` directory)
- **Frontend**: React + Vite application (`/eventease-frontend` directory)

## Step-by-Step Deployment

### 1. Prepare Your Environment Variables

Before deploying, you'll need these API keys and configuration:

**Required Secrets:**

- `GRADIENT_API_KEY`: Your Gradient AI API key
- `GRADIENT_EMBEDDING_MODEL`: The embedding model name from Gradient AI

**Example values:**

```
GRADIENT_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
GRADIENT_EMBEDDING_MODEL=text-embedding-ada-002
```

### 2. Deploy to DigitalOcean App Platform

#### Option A: Using the DigitalOcean Dashboard (Recommended)

1. **Login to DigitalOcean**

   - Go to https://cloud.digitalocean.com/
   - Navigate to "Apps" in the left sidebar

2. **Create a New App**

   - Click "Create App"
   - Choose "GitHub" as your source
   - Select your repository: `AnimeshNilawar/EventEase-Ai-Bot`
   - Choose the `main` branch

3. **Configure App Specification**

   - DigitalOcean will detect your `.do/app.yaml` file automatically
   - Review the configuration:
     - Backend service (FastAPI)
     - Frontend static site (React)

4. **Set Environment Variables**

   - In the app configuration, go to "Environment Variables"
   - Add the following **encrypted** variables:
     ```
     GRADIENT_API_KEY=your_actual_api_key_here
     GRADIENT_EMBEDDING_MODEL=your_embedding_model_name
     ```

5. **Deploy**
   - Review your configuration
   - Click "Create Resources"
   - Wait for deployment to complete (usually 5-10 minutes)

#### Option B: Using DigitalOcean CLI (doctl)

1. **Install and Configure doctl**

   ```bash
   # Install doctl
   # On Windows (PowerShell):
   Invoke-WebRequest -Uri "https://github.com/digitalocean/doctl/releases/latest/download/doctl-1.100.0-windows-amd64.zip" -OutFile "doctl.zip"
   Expand-Archive doctl.zip

   # Authenticate
   doctl auth init
   ```

2. **Deploy using App Spec**

   ```bash
   doctl apps create --spec .do/app.yaml
   ```

3. **Set Environment Variables**

   ```bash
   # Get your app ID
   doctl apps list

   # Update environment variables
   doctl apps update YOUR_APP_ID --spec .do/app.yaml
   ```

### 3. Post-Deployment Configuration

#### Update Frontend API URL

After deployment, you'll get URLs for your services:

- Backend: `https://backend-xxxxx.ondigitalocean.app`
- Frontend: `https://frontend-static-xxxxx.ondigitalocean.app`

The frontend will automatically use the backend URL via the `VITE_API_URL` environment variable set in the app spec.

#### Test Your Deployment

1. **Health Check**

   - Visit: `https://your-backend-url.ondigitalocean.app/health`
   - Should return: `{"status": "ok", "service": "EventEase", "version": "0.1"}`

2. **Frontend**
   - Visit your frontend URL
   - Test the chat functionality
   - Try uploading a PDF file

### 4. Domain Configuration (Optional)

To use a custom domain:

1. **Add Domain in DigitalOcean**

   - Go to your app settings
   - Click "Domains"
   - Add your custom domain

2. **Update DNS**

   - Add CNAME records pointing to your app URLs

3. **Update CORS Settings**
   - Update `FRONTEND_ORIGIN` environment variable to your custom domain

## Environment Variables Reference

### Backend Environment Variables

```yaml
DEBUG: "False" # Production mode
FRONTEND_ORIGIN: "${APP_DOMAIN}" # Auto-set by DO
DATA_DIR: "/tmp/data" # Temporary storage
VECTOR_DIR: "/tmp/data/vector_store" # Vector database storage
USE_GRADIENT: "True" # Enable Gradient AI
GRADIENT_API_BASE: "https://inference.do-ai.run"
GRADIENT_MODEL: "gpt-4o-mini" # Chat model
USE_GRADIENT_EMBEDDINGS: "True" # Use Gradient embeddings
GRADIENT_API_KEY: "SECRET" # Your API key (encrypted)
GRADIENT_EMBEDDING_MODEL: "SECRET" # Model name (encrypted)
```

### Frontend Environment Variables

```yaml
VITE_API_URL: "${backend.PUBLIC_URL}" # Auto-set to backend URL
```

## Monitoring and Logs

### View Application Logs

```bash
# Using doctl
doctl apps logs YOUR_APP_ID --type=run

# Or via dashboard
# Go to your app > Runtime Logs
```

### Monitor Resources

- CPU and Memory usage available in the dashboard
- Set up alerts for high resource usage

## Troubleshooting

### Common Issues

1. **Build Failures**

   - Check that all dependencies are in requirements.txt
   - Ensure Python version compatibility

2. **API Connection Issues**

   - Verify GRADIENT_API_KEY is set correctly
   - Check network connectivity to Gradient AI

3. **CORS Errors**

   - Ensure FRONTEND_ORIGIN matches your frontend URL
   - Check allowed origins in main.py

4. **File Upload Issues**
   - Note: Uploaded files are stored in `/tmp` and may be lost on restart
   - Consider using DigitalOcean Spaces for persistent storage

### Logs and Debugging

```bash
# View real-time logs
doctl apps logs YOUR_APP_ID --follow

# Check specific service logs
doctl apps logs YOUR_APP_ID --type=build
doctl apps logs YOUR_APP_ID --type=deploy
```

## Scaling and Performance

### Automatic Scaling

- DigitalOcean App Platform automatically scales based on traffic
- Configure in app settings if needed

### Performance Optimization

- Vector database is loaded into memory on startup
- Consider upgrading instance size for large datasets
- Use CDN for frontend assets (auto-enabled for static sites)

## Cost Optimization

- **Basic XXS instances** are sufficient for development
- **Basic XS or S** recommended for production
- Monitor usage in the billing dashboard

## Security Best practices

1. **Environment Variables**

   - Always use encrypted environment variables for API keys
   - Never commit secrets to your repository

2. **CORS Configuration**

   - Restrict origins in production
   - Don't use wildcard (\*) in production

3. **API Rate Limiting**
   - Consider implementing rate limiting for the chat endpoint
   - Monitor API usage and costs

## Support

- **DigitalOcean Support**: Available through the dashboard
- **Community**: DigitalOcean Community forums
- **Documentation**: [App Platform docs](https://docs.digitalocean.com/products/app-platform/)

---

## Quick Deployment Checklist

- [ ] Repository is public or DigitalOcean has access
- [ ] `.do/app.yaml` is in repository root
- [ ] Gradient AI API key obtained
- [ ] Environment variables configured
- [ ] App deployed successfully
- [ ] Health endpoint returns 200
- [ ] Frontend loads correctly
- [ ] Chat functionality works
- [ ] File upload works

Your EventEase AI Bot should now be live and accessible via the provided URLs!
