from datetime import datetime

from pydantic import BaseModel


class SessionCreate(BaseModel):
    title: str
    description: str | None = None
    scheduled_at: datetime


class SessionResponse(BaseModel):
    id: int
    teacher_id: int
    title: str
    description: str | None
    status: str
    scheduled_at: datetime

    model_config = {
        "from_attributes": True
    }