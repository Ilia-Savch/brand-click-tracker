from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ClickResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    click_id: UUID
    offer: str
    sub1: str
    timestamp: datetime
    ip: str
    user_agent: str