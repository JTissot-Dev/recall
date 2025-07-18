from typing import List, Optional
import uuid
from app.protocols.i_ollama_provider import IOllamaProvider
from app.schemas import (
    ChatMessage,
    ChatResponse,
    ConversationResponse,
    MessageCreate,
    ConversationCreate,
)
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService


class ChatService:
    def __init__(
        self,
        ollama_provider: IOllamaProvider,
        conversation_service: ConversationService,
        message_service: MessageService,
    ):
        self.ollama_provider = ollama_provider
        self.conversation_service = conversation_service
        self.message_service = message_service
        self.chat_history: List[ChatMessage] = []

    def init_chat_session(
        self, conversation_id: Optional[str] = None
    ) -> ConversationResponse:
        """
        Initialize a chat session.
        """
        if conversation_id:
            conversation = self.conversation_service.read_by_id(conversation_id)
            self.chat_history.extend(
                ChatMessage.model_validate(msg) for msg in conversation.messages
            )
        else:
            title = f"Conversation {uuid.uuid4().hex[:6]}"
            conversation = self.conversation_service.create(
                ConversationCreate(title=title)
            )
        return conversation

    def process_chat_session(
        self, client_msg: str, conversation: ConversationResponse
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

        self.chat_history.append(ChatMessage.model_validate(user_message))

        bot_msg = self.ollama_provider.process_chat_message(
            client_msg, self.chat_history
        )

        assistant_message = self.message_service.create(
            MessageCreate(
                conversation_id=conversation.id,
                role="assistant",
                content=bot_msg.response,
            )
        )
        self.chat_history.append(ChatMessage.model_validate(assistant_message))

        return bot_msg
