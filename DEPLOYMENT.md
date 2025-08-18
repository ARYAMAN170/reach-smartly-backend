# Deployment Guide for Render

## Prerequisites
1. Create a [Render](https://render.com) account
2. Have your API keys ready (Gemini, OpenAI, Firebase credentials)

## Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create Web Service on Render
1. Go to your Render dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `smart-outreach-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Set Environment Variables
In the Render dashboard, add these environment variables:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `SERPER_API_KEY`: Your Serper API key for company search functionality
- `OPENAI_API_KEY`: Your OpenAI API key (if used)
- `FIREBASE_CREDENTIALS`: Your Firebase service account JSON (as a string)
- `PYTHON_VERSION`: `3.10`

### 4. Deploy
Click "Deploy" and wait for the deployment to complete.

## Alternative: Using render.yaml
You can also deploy using the included `render.yaml` file:

1. Push the `render.yaml` file to your repository
2. In Render dashboard, choose "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically read the configuration from `render.yaml`

## Post-Deployment
- Your API will be available at: `https://your-service-name.onrender.com`
- Test the health endpoint: `https://your-service-name.onrender.com/health`
- Update CORS origins in `app/core/config.py` if needed

## Important Notes
- Free tier on Render has limitations (sleeps after 15 minutes of inactivity)
- Make sure all environment variables are set correctly
- Monitor logs in the Render dashboard for any issues
- The app will automatically create the `uploaded_pdfs` directory on startup
