from app.models.hr_contact import HRContact
from app.models.email import EmailRequest
from app.models.email_send import EmailSendRequest # Import the new model
from app.services.email_service import generate_outreach_email
from fastapi import APIRouter, HTTPException
from app.services.gmail_sender import get_gmail_service, create_message, create_message_with_attachment, send_message
import base64

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
        return email_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-email")
async def send_email(request: EmailSendRequest):
    service = get_gmail_service()
    email_message = None

    if request.attachResume and request.resumeAttachment:
        try:
            # Decode the Base64 content to bytes
            attachment_data = base64.b64decode(request.resumeAttachment.content)
            email_message = create_message_with_attachment(
                sender=request.from_field,
                to=request.to,
                subject=request.subject,
                message_text=request.body,
                attachment_data=attachment_data,
                filename=request.resumeAttachment.filename,
                content_type=request.resumeAttachment.contentType
            )
        except (ValueError, TypeError) as e:
            raise HTTPException(status_code=400, detail=f"Invalid Base64 attachment content: {e}")
    else:
        # Create a simple email without an attachment
        email_message = create_message(
            sender=request.from_field,
            to=request.to,
            subject=request.subject,
            message_text=request.body
        )

    if not email_message:
        raise HTTPException(status_code=500, detail="Failed to create email message.")

    # Send the message and return the result
    result = send_message(service, "me", email_message)
    if result:
        return {"status": "success", "message_id": result['id']}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email via Gmail API.")