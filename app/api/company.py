from fastapi import APIRouter, HTTPException, Query
from app.services.company_scraper import get_company_website, get_company_overview

router = APIRouter()


@router.get("/company-overview")
def fetch_company_overview(company_name: str = Query(..., description="Name of the company")):
    website = get_company_website(company_name)

    if not website:
        raise HTTPException(status_code=404, detail="Company website not found.")

    overview = get_company_overview(website)
    if not overview:
        raise HTTPException(status_code=404, detail="Company overview not found.")

    return overview  # ✅ Return as JSON object
