from fastapi import APIRouter
from app.api.routes.message import router as message_router


api_router = APIRouter(prefix="/api")
api_router.include_router(message_router)
