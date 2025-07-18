from typing import Annotated
from fastapi import Depends
from app.providers.deps import OllamaProviderDep
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService
from app.services.chat_service import ChatService


def get_chat_service(
    ollama_provider: OllamaProviderDep,
    conversation_service: ConversationService = Depends(),
    message_service: MessageService = Depends(),
) -> ChatService:
    return ChatService(ollama_provider, conversation_service, message_service)

ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]