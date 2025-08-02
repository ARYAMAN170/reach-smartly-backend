# Smart Outreach Backend API

AI-powered email outreach and resume parsing API built with FastAPI.

## Features

- **HR Contact Parsing**: Extract HR contacts from PDF files
- **Resume Analysis**: Parse and extract information from PDF resumes  
- **AI Email Generation**: Generate personalized outreach emails using Google's Gemini AI
- **Multiple Email Types**: Support for introduction, follow-up, and thank-you emails

## Quick Deploy on Render

### Step 1: Prepare Your Repository
1. Push this code to your GitHub repository
2. Make sure all files are committed and pushed

### Step 2: Create Render Service
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your repository from the list

### Step 3: Configure Service
1. **Name**: `reach-smartly-backend` (or any name you prefer)
2. **Root Directory**: `auto_email` (important!)
3. **Environment**: `Python 3`
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Render will automatically start building and deploying
3. Wait for the build to complete (usually 2-5 minutes)

### Step 5: Test Your API
Once deployed, your API will be available at:
- **Base URL**: `https://your-service-name.onrender.com`
- **Health Check**: `https://your-service-name.onrender.com/health`
- **API Docs**: `https://your-service-name.onrender.com/docs`

## API Endpoints

### Health Check
- `GET /` - Basic API information
- `GET /health` - Health check endpoint

### HR Contacts  
- `POST /api/hr/upload-hr/` - Upload PDF and extract HR contacts

### Resume Processing
- `POST /api/extract-resume` - Extract information from resume PDF

### Email Generation
- `POST /api/generate-email` - Generate personalized outreach emails

## Local Development

1. **Clone and navigate**:
   ```bash
   git clone <your-repo>
   cd auto_email
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access locally**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

## Tech Stack

- **FastAPI**: Modern Python web framework
- **Google Gemini AI**: For intelligent email generation
- **PyMuPDF**: PDF text extraction
- **Camelot**: Table extraction from PDFs
- **Pydantic**: Data validation and serialization

## Troubleshooting

### Common Issues:
1. **Build fails**: Check that `auto_email` is set as root directory
2. **Import errors**: Ensure all dependencies are in requirements.txt
3. **Port issues**: Render automatically provides $PORT environment variable

### Support
For issues, check the Render logs in your dashboard or create an issue in the repository.