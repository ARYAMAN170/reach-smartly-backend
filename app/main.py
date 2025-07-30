from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import both routers
from app.api.routes_hr import router as hr_router
from app.api.routes_email import router as email_router
from app.api.routes_resume import router as resume_router
# Initialize the FastAPI app
app = FastAPI(title="Smart Outreach API")

# CORS (Cross-Origin Resource Sharing) configuration
# This allows your frontend (e.g., running on localhost:8080) to communicate with your backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://reach-smartly.vercel.app",                       # no trailing slash
        "https://reach-smartly-git-main-aryaman170s-projects.vercel.app"
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",                # catch any other Vercel preview URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the different routers from your application
# It's good practice to add a prefix and tags for organization
app.include_router(hr_router, prefix="/api/hr", tags=["HR Contacts"])
app.include_router(email_router, prefix="/api", tags=["Email Generation"])
app.include_router(resume_router, prefix="/api", tags=["Resume Skills"])
# Optional: Add a root endpoint for basic health checks
@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Outreach API"}

