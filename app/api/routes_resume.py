from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.services.resume import extract_user_summary_from_pdf_upload

router = APIRouter()


@router.post("/extract-resume")
async def extract_resume(file: UploadFile = File(...)):
    """
    Extract user details and professional summary from uploaded PDF resume.

    Args:
        file: PDF file upload

    Returns:
        JSON response with extracted user details or error message
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Validate file size (optional - adjust as needed)
    if file.size and file.size > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(
            status_code=400,
            detail="File size too large. Maximum 10MB allowed."
        )

    try:
        result = await extract_user_summary_from_pdf_upload(file)

        # Check if result contains an error
        if isinstance(result, dict) and "error" in result:
            return JSONResponse(
                status_code=400,
                content=result
            )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": result,
                "message": "Resume processed successfully"
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": f"Internal server error: {str(e)}"
            }
        )