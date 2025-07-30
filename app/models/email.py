from pydantic import BaseModel
from typing import Optional

class EmailRequest(BaseModel):
    full_name: str
    email: str
    company_name: str
    job_title: Optional[str] = None
    notes: Optional[str] = None
    user_summary: str
    user_name: str
    email_type: str
