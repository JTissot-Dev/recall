from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.database import SessionDep
from app.services.chat_service import ChatService
from app.providers.ollama_provider import OllamaProvider
from app.schemas import ChatWebSocketResponse
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService
from app.models import Conversation, Message

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: SessionDep):
    """
    WebSocket endpoint for real-time chat.
    """
    ollama_provider = OllamaProvider(temperature=0.7)  
    chat_service = ChatService(ollama_provider)  
    conversation_service = ConversationService(session)
    message_service = MessageService(session)
    chat_history = []
    await websocket.accept()

    try:
        while True:
            client_msg = await websocket.receive_text()
            bot_msg = await chat_service.process_llm_message(client_msg, chat_history)
            chat_history = bot_msg.updated_history

            response = ChatWebSocketResponse(
                type="message",
                content=bot_msg.response,
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            await websocket.send_text(response.model_dump_json())
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        
        if chat_history:
            new_conversation = conversation_service.create(
                Conversation(title="New")
            )
            conversation_messages = [
                Message(
                    conversation_id=new_conversation.id,
                    role=message.role,
                    content=message.content
                ) for message in chat_history
            ]
            message_service.create_many(conversation_messages)

    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close(code=1000, reason=str(e))