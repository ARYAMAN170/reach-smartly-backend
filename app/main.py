import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Import all routers
from app.api.routes_hr import router as hr_router
from app.api.routes_email import router as email_router
from app.api.routes_resume import router as resume_router
from app.api.company import router as company_router

# Initialize the FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS (Cross-Origin Resource Sharing) configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",  # catch any other Vercel preview URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the different routers from your application
app.include_router(hr_router, prefix="/api/hr", tags=["HR Contacts"])
app.include_router(email_router, prefix="/api", tags=["Email Generation"])
app.include_router(resume_router, prefix="/api", tags=["Resume Skills"])
app.include_router(company_router, prefix="/api", tags=["Company"])

# Health check endpoint
@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "healthy"
    }

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring services."""
    return {"status": "healthy", "service": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

