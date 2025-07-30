import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from app.models.hr_contact import HRContact
from app.services.hr_parser import parse_hr_contacts_pdf
from app.utils.file_handler import save_uploaded_file, delete_file

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.post("/upload-hr/", response_model=List[HRContact])
async def upload_pdf_and_parse(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        file_path = save_uploaded_file(UPLOAD_DIR, file)
        hr_contacts = parse_hr_contacts_pdf(file_path)

        if not hr_contacts:
            raise HTTPException(status_code=404, detail="No HR contacts found.")

        return hr_contacts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
    finally:
        delete_file(file_path)
