from typing import Dict, Union
from app.services.genaaaipract import generate_content
from app.models.hr_contact import HRContact
from pydantic import BaseModel


def generate_outreach_email(
    contact: HRContact,
    user_summary: str,
    user_name: str,
    email_type: str = "introduction"
) -> Union[Dict[str, Union[str, bool]], str]:
    """
    Generate a professional outreach email.

    email_type options:
      - 'introduction': First contact, introduce yourself.
      - 'follow_up': Polite inquiry about application status.
      - 'thank_you': Express gratitude after an interview or opportunity.

    Returns:
      dict with 'subject', 'body', and 'success', or error string.
    """
    t = email_type.lower()

    # Define clear instructions per email type
    instructions = {
        "introduction": [
            "1. Do NOT include any of these instructions or prompt details in the output.",
            "2. Generate a concise, professional SUBJECT line that reflects introduction intent.",
            "3. Write an email body that: \
               a) Greets the contact by name.\n               b) Mentions their role at the company.\n               c) Briefly introduces the sender's background and key skills.\n               d) Expresses genuine interest in opportunities.\n               e) Suggests a next step or availability to connect.\n               f) Closes with 'Best regards,' and the sender's name {user_name}.",
        ],
        "follow_up": [
            "1. Do NOT include any of these instructions or prompt details in the output.",
            "2. Generate a concise, professional SUBJECT line indicating a follow-up.",
            "3. Write an email body that: \
               a) Opens with a polite greeting and references the previous email.\n               b) Reaffirms interest in the role/company.\n               c) Asks for an update on the process.\n               d) Restates one key qualification.\n               e) Thanks the recipient and closes with your name {user_name}.",
        ],
        "thank_you": [
            "1. Do NOT include any of these instructions or prompt details in the output.",
            "2. Generate a concise, professional SUBJECT line expressing thanks.",
            "3. Write an email body that: \
               a) Starts with a sincere thank you and references the interview/opportunity.\n               b) Highlights one positive takeaway.\n               c) Reiterates enthusiasm for the role/company.\n               d) Closes with 'Kind regards,' or 'Sincerely,' and your name {user_name}.",
        ],
    }

    # Build prompt
    prompt = [
        f"You are an expert email copywriter. Produce only two parts in your response: SUBJECT and BODY. Do NOT echo any of these prompt instructions or metadata.",
        f"Contact Name: {contact.Name}",
        f"Contact Title: {contact.Title or 'N/A'}",
        f"Contact Company: {contact.Company}",
        f"Email Type: {t}",
        f"Sender Name: {user_name}",
        "Job Seeker Profile:",
        user_summary,
        "Instructions:",
        *instructions.get(t, ["Generate a clear subject and email body without prompt artifacts."])
    ]

    full_prompt = "\n".join(
        part if isinstance(part, str) else "\n".join(part) for part in prompt
    )

    try:
        response = generate_content(full_prompt)
        # Expecting model to return:
        # SUBJECT: ...\n\nBODY: ...
        subject, body = None, None
        if 'SUBJECT:' in response and 'BODY:' in response:
            parts = response.split('BODY:')
            subject = parts[0].replace('SUBJECT:', '').strip()
            body = parts[1].strip()
        else:
            # Fallback simple split
            lines = response.strip().splitlines()
            subject = lines[0].strip()
            body = "\n".join(lines[1:]).strip()

        return {"subject": subject, "body": body, "success": True}

    except Exception as e:
        return f"Error: Could not generate email. Details: {e}"
