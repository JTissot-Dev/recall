from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from app.schemas.message import MessageResponse


class ConversationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)

class ConversationResponse(BaseModel):
    id: UUID
    title: str
    messages: list[MessageResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}