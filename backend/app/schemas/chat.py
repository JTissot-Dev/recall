from typing import List
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str

    model_config = {"from_attributes": True}


class ChatResponse(BaseModel):
    response: str
    updated_history: List[ChatMessage]

    model_config = {"from_attributes": True}


class ChatWebSocketResponse(BaseModel):
    type: str
    content: str
    timestamp: str
