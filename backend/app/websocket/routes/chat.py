from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Optional
import uuid
from app.core.database import SessionDep
from app.core.websocket.connection_manager import manager
from app.services.chat_service import ChatService
from app.providers.ollama_provider import OllamaProvider
from app.schemas import (
    ChatWebSocketResponse,
    ConversationCreate,
    ChatMessage
)
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket, 
    session: SessionDep, 
    conversation_id: Optional[str] = None  
):
    """
    WebSocket endpoint for real-time chat.
    """
    await manager.connect(websocket)
    print(conversation_id)
    ollama_provider = OllamaProvider(temperature=0.7)
    conversation_service = ConversationService(session)
    message_service = MessageService(session)

    chat_service = ChatService(
        ollama_provider,
        conversation_service,
        message_service
    )

    chat_history = []

    if conversation_id:
        conversation = conversation_service.read_by_id(conversation_id)
        chat_history.extend(
            ChatMessage(**msg.model_dump()) for msg in
            conversation.messages
        )
    else:
        title = f"Conversation {uuid.uuid4().hex[:6]}"
        conversation = conversation_service.create(
            ConversationCreate(title=title)
        )

    try:
        while True:
            client_msg = await websocket.receive_text()

            bot_msg = chat_service.chat_session(
                client_msg,
                chat_history,
                conversation
            )

            response = ChatWebSocketResponse(
                type="message",
                content=bot_msg.response,
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
            await manager.send_personal_message(
                response.model_dump_json(), websocket
            )

    except WebSocketDisconnect:
        print("WebSocket disconnected")
        manager.disconnect(websocket)

    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
