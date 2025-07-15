from typing import List
from app.protocols.i_ollama_provider import IOllamaProvider
from app.schemas import (
    ChatMessage,
    ChatResponse,
    ConversationResponse,
    MessageCreate,
)
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService


class ChatService:
    def __init__(
        self,
        ollama_provider: IOllamaProvider,
        conversation_service: ConversationService,
        message_service: MessageService
    ):
        self.ollama_provider = ollama_provider
        self.conversation_service = conversation_service
        self.message_service = message_service

    def chat_session(
        self, 
        client_msg: str, 
        chat_history: List[ChatMessage],
        conversation: ConversationResponse
    ) -> ChatResponse:
        """
        Handle a complete chat session.
        """
        user_message = self.message_service.create(
            MessageCreate(
                conversation_id=conversation.id,
                role="user",
                content=client_msg,
            )
        )
        
        chat_history.append(
            ChatMessage(**user_message.model_dump())
        )

        bot_msg = self.ollama_provider.process_chat_message(
            client_msg, chat_history
        )

        assistant_message = self.message_service.create(
            MessageCreate(
                conversation_id=conversation.id,
                role="assistant",
                content=bot_msg.response,
            )
        )
        chat_history.append(
            ChatMessage(**assistant_message.model_dump())
        )

        return bot_msg