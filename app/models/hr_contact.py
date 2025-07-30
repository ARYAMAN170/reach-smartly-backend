from pydantic import BaseModel

class HRContact(BaseModel):
    Name: str
    Email: str
    Title: str
    Company: str
