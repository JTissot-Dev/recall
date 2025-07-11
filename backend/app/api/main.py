from fastapi import APIRouter


api_router = APIRouter(prefix="/api", tags=["API"])
# api_router.include_router() // Exemple new route
