from app.schemas.chat import ChatMessage, ChatResponse
from typing import List, Protocol


class IOllamaProvider(Protocol):
    """Protocol for all LLM providers - just the interface"""
    
    def process_chat_message(self, message: str, history: List[ChatMessage] = None) -> ChatResponse:
        """Process a chat message and return the bot's response"""
        ...