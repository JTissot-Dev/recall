from typing import List
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatResponse(BaseModel):
    response: str
    updated_history: List[ChatMessage]


class ChatWebSocketResponse(BaseModel):
    type: str
    content: str
    timestamp: str
