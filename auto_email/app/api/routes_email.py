from fastapi import APIRouter, HTTPException
from app.models.hr_contact import HRContact
from app.models.email import EmailRequest  # ✅ imported from models
from app.services.email_service import generate_outreach_email

router = APIRouter()


@router.post("/generate-email")
async def generate_email(data: EmailRequest):
    try:
        contact = HRContact(
            Name=data.full_name,
            Email=data.email,
            Title=data.job_title or "",
            Company=data.company_name
        )

        email_result = generate_outreach_email(contact, data.user_summary, data.user_name)

        return email_result  # Return the dict directly

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))