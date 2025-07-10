from sqlmodel import Session
from typing import List, Optional
from app.protocols.i_ollama_provider import IOllamaProvider
from app.schemas import ChatMessage, ChatResponse


class ChatService:
    def __init__(
            self, 
            ollama_provider: Optional[IOllamaProvider] = None, 
        ):
        self.ollama_provider = ollama_provider

    async def process_llm_message(self, client_msg: str, chat_history: List[ChatMessage] = None) -> ChatResponse:
        """
        Process a chat message and return the bot's response.
        """
        bot_msg = self.ollama_provider.process_chat_message(client_msg, chat_history)
        return bot_msg

    
