from fastapi import APIRouter
from app.api.routes.auth import router as auth_router
from app.api.routes.user import router as user_router


api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(user_router)
