from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from app.enums import Role


class MessageCreate(BaseModel):
    role: Role
    content: str
    conversation_id: UUID

class MessageResponse(BaseModel):
    id: UUID
    role: Role
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
