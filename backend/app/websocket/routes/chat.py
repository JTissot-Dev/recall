import logging
from datetime import datetime, timezone
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Optional
from app.core.websocket.connection_manager import manager
from app.services.deps import ChatServiceDep
from app.schemas import ChatWebSocketResponse


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_service: ChatServiceDep,
    conversation_id: Optional[str] = None,
):
    """
    WebSocket endpoint for real-time chat.
    """
    await manager.connect(websocket)
    conversation = chat_service.init_chat_session(conversation_id)

    try:
        while True:
            client_msg = await websocket.receive_text()
            bot_msg = chat_service.process_chat_session(
                client_msg, conversation
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
        manager.disconnect(websocket)

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
