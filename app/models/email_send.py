from pydantic import BaseModel, Field
from typing import Optional


class ResumeAttachment(BaseModel):
    content: str
    filename: str
    contentType: str


class EmailSendRequest(BaseModel):
    to: str
    toName: str
    subject: str
    body: str
    from_field: str = Field(..., alias="from")
    fromName: str
    companyName: str
    contactId: str
    attachResume: bool
    userId: str
    resumeUrl: Optional[str] = None
    resumeAttachment: Optional[ResumeAttachment] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {"example": {"from": "example@gmail.com"}}