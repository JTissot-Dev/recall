from fastapi import APIRouter
from app.websocket.routes.chat import router

ws_router = APIRouter(prefix="/ws", tags=["WebSocket"])
ws_router.include_router(router)