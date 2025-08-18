from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
from app.services.company_scraper import get_company_info

router = APIRouter()


@router.get("/company-overview", response_model=Dict[str, Any])
def fetch_company_overview(company_name: str = Query(..., description="Name of the company")):
    """
    Fetch comprehensive company information including website and overview.
    
    Args:
        company_name: Name of the company to search for
        
    Returns:
        Dictionary containing company information
        
    Raises:
        HTTPException: If company information cannot be found or API key is missing
    """
    try:
        company_info = get_company_info(company_name)
        
        if not company_info["success"]:
            # Determine appropriate HTTP status code based on error type
            if "API" in company_info.get("error", "") or "key" in company_info.get("error", ""):
                status_code = 500  # Server configuration error
                detail = "Service configuration error. Please contact administrator."
            else:
                status_code = 404  # Company not found
                detail = company_info.get("error", "Company information not found")
                
            raise HTTPException(status_code=status_code, detail=detail)
        
        return {
            "company_name": company_info["company_name"],
            "website": company_info["website"],
            "overview": company_info["overview"],
            "success": True
        }
        
    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected error occurred while fetching company information: {str(e)}"
        )


@router.get("/company-website", response_model=Dict[str, Any])
def fetch_company_website(company_name: str = Query(..., description="Name of the company")):
    """
    Fetch only the company website URL.
    
    Args:
        company_name: Name of the company to search for
        
    Returns:
        Dictionary containing company website information
    """
    from app.services.company_scraper import get_company_website
    
    try:
        website = get_company_website(company_name)
        
        if not website:
            raise HTTPException(
                status_code=404, 
                detail=f"Website not found for company: {company_name}"
            )
        
        return {
            "company_name": company_name,
            "website": website,
            "success": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching for company website: {str(e)}"
        )
