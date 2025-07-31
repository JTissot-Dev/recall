from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import Annotated
from app.api.deps import get_current_active_user
from app.schemas import UserPayload

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserPayload)
async def get_current_user(
    current_user: Annotated[UserPayload, Depends(get_current_active_user)]
):
    """
    Get the current authenticated user.
    """
    return current_user