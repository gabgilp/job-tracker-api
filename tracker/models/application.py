from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ApplicationIn(BaseModel):
    user_id: int
    company_name: str
    position_title: str
    status: str
    notes: str
    date_applied: datetime
    posting_url: str

class Application(ApplicationIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    rejection_reason: str | None = None
    rejection_date: datetime | None = None

class ApplicationResponse(BaseModel):
    new_token: str
    token_type: str
    application: Application