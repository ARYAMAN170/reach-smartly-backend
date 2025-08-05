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
            "1. SUBJECT: Directly address the person by name and include how you can be useful to their company. Use "
            "simple, powerful words.",
            "2. BODY: Write three concise paragraphs:\n   a) Short self-introduction highlighting one key achievement "
            "and clearly state: 'I am seeking an internship opportunity and would appreciate an interview.'\n   b) "
            "Explain why you are contacting them specifically and what excites you about working at their company.\n  "
            " c) Ask what you need from them: 'How can I start the interview process?'. End with a simple question If "
            "they can be helpful regarding this matter'\n",
            "3. First line of the body must grab attention by stating how your skills will impact their team.\n4. "
            "Close with 'Best regards,' followed by {user_name}."
        ],
        "follow_up": [
            "1. SUBJECT: Polite follow-up regarding internship inquiry at {contact.Company}.",
            "2. BODY: Open with greeting referencing previous email.\n   a) Reaffirm interest in the internship.\n   "
            "b) Restate one key qualification.\n   c) Politely ask for an update: 'I know you're busy, but could you "
            "please let me know the status?'\n3. Close with 'Best regards,' and {user_name}."
        ],
        "thank_you": [
            "1. SUBJECT: Thank you for your time, {contact.Name}.",
            "2. BODY: Thank them for the opportunity, mention a positive takeaway, and reiterate enthusiasm.\n3. "
            "Close with 'Sincerely,' or 'Kind regards,' and {user_name}."
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

