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
