from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import uuid
from app.core.database import SessionDep
from app.core.websocket.connection_manager import manager
from app.services.chat_service import ChatService
from app.providers.ollama_provider import OllamaProvider
from app.schemas import (
    ChatWebSocketResponse,
    ChatMessage,
    MessageCreate,
    ConversationCreate
)
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket, session: SessionDep
):
    """
    WebSocket endpoint for real-time chat.
    """
    await manager.connect(websocket)

    ollama_provider = OllamaProvider(temperature=0.7)
    chat_service = ChatService(ollama_provider)
    conversation_service = ConversationService(session)
    message_service = MessageService(session)


    title = f"Conversation {uuid.uuid4().hex[:6]}"
    new_conversation = conversation_service.create(
        ConversationCreate(title=title)
    )

    chat_history = []

    try:
        while True:
            client_msg = await websocket.receive_text()

            user_message = message_service.create(
                MessageCreate(
                    conversation_id=new_conversation.id,
                    role="user",
                    content=client_msg,
                )
            )
            chat_history.append(
                ChatMessage(**user_message.model_dump())
            )

            bot_msg = await chat_service.process_llm_message(
                client_msg, chat_history
            )

            assistant_message = message_service.create(
                MessageCreate(
                    conversation_id=new_conversation.id,
                    role="assistant",
                    content=bot_msg.response,
                )
            )

            chat_history.append(
                ChatMessage(**assistant_message.model_dump())
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
