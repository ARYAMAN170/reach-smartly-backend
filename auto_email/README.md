# Smart Outreach Backend API

AI-powered email outreach and resume parsing API built with FastAPI.

## Features

- **HR Contact Parsing**: Extract HR contacts from PDF files
- **Resume Analysis**: Parse and extract information from PDF resumes
- **AI Email Generation**: Generate personalized outreach emails using Google's Gemini AI
- **Multiple Email Types**: Support for introduction, follow-up, and thank-you emails

## Deployment on Render

### Prerequisites

1. A Render account
2. Google Gemini API key

### Deploy Steps

1. **Fork/Clone this repository**

2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the `auto_email` folder as the root directory

3. **Configure Environment Variables**:
   - In Render dashboard, go to your service settings
   - Add environment variable:
     - `GEMINI_API_KEY`: Your Google Gemini API key

4. **Deploy**:
   - Render will automatically detect the `render.yaml` file
   - The service will build and deploy automatically

### Local Development

1. **Install dependencies**:
   ```bash
   cd auto_email
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Run the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

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

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for AI email generation | Yes |

## Tech Stack

- **FastAPI**: Modern Python web framework
- **Google Gemini AI**: For intelligent email generation
- **PyMuPDF**: PDF text extraction
- **Camelot**: Table extraction from PDFs
- **Pydantic**: Data validation and serialization

## Support

For issues and questions, please create an issue in the repository.