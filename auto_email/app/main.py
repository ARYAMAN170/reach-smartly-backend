from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import routers
from app.api.routes_hr import router as hr_router
from app.api.routes_email import router as email_router
from app.api.routes_resume import router as resume_router

# Initialize the FastAPI app
app = FastAPI(
    title="Smart Outreach API",
    description="AI-powered email outreach and resume parsing API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost:5173",
        "https://reach-smartly.vercel.app",
        "https://reach-smartly-git-main-aryaman170s-projects.vercel.app",
        "https://*.onrender.com"
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hr_router, prefix="/api/hr", tags=["HR Contacts"])
app.include_router(email_router, prefix="/api", tags=["Email Generation"])
app.include_router(resume_router, prefix="/api", tags=["Resume Skills"])

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Smart Outreach API",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Smart Outreach API"}