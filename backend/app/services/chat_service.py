from sqlmodel import Session
from typing import List, Optional
import uuid
from app.models import Conversation
from app.protocols.i_ollama_provider import IOllamaProvider
from app.schemas import (
    ChatMessage,
    ChatResponse,
    ConversationResponse,
    MessageCreate,
    ConversationCreate,
)
from app.repositories.conversation_repository import create_conversation, read_conversation_by_id
from app.repositories.message_repository import create_message


class ChatService:
    def __init__(
        self,
        ollama_provider: IOllamaProvider,
    ):
        self.ollama_provider = ollama_provider
        self.chat_history: List[ChatMessage] = []

    def init_chat_session(
        self, session: Session, conversation_id: Optional[str] = None
    ) -> Conversation:
        """
        Initialize a chat session.
        """
        if conversation_id:
            conversation = read_conversation_by_id(session, conversation_id)
            self.chat_history.extend(
                ChatMessage.model_validate(msg) for msg in conversation.messages
            )
        else:
            title = f"Conversation {uuid.uuid4().hex[:6]}"
            conversation = create_conversation(
                session, ConversationCreate(title=title)
            )
        return conversation

    def process_chat_session(
        self, session: Session, client_msg: str, conversation: ConversationResponse
    ) -> ChatResponse:
        """
        Handle a complete chat session.
        """
        user_message = create_message(
            session,
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

        assistant_message = create_message(
            session,
            MessageCreate(
                conversation_id=conversation.id,
                role="assistant",
                content=bot_msg.response,
            )
        )
        self.chat_history.append(ChatMessage.model_validate(assistant_message))

        return bot_msg
