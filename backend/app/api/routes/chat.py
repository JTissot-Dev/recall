from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket
from app.core.database import SessionDep
from app.services.chat_service import ChatService
from app.providers.ollama_provider import OllamaProvider
from app.schemas.chat import ChatWebSocketResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/")
async def get_chat():
    """
    Endpoint to retrieve chat information.
    """
    return {"message": "Chat endpoint is working!"}

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: SessionDep):
    """
    WebSocket endpoint for real-time chat.
    """
    ollama_provider = OllamaProvider(temperature=0.7)  
    chat_service = ChatService(ollama_provider, session)  
    chat_history = []
    await websocket.accept()

    try:
        while True:
            client_msg = await websocket.receive_text()
            bot_msg = chat_service.process_llm_message(client_msg, chat_history)
            chat_history = bot_msg.updated_history

            response = ChatWebSocketResponse(
                type="message",
                content=bot_msg.response,
                timestamp=datetime.now(timezone.utc).isoformat()
            )
            await websocket.send_text(response.model_dump_json())
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close(code=1000, reason=str(e))