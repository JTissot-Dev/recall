import logging
from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from app.core.database import SessionDep
from app.services.message_service import read_paginate_message
from app.schemas import MessagesPaginateResponse


router = APIRouter(prefix="/messages", tags=["Messages"])

logger = logging.getLogger(__name__)


@router.get("", response_model=MessagesPaginateResponse, status_code=200)
def read_messages(
    session: SessionDep,
    conversation_id: str,
    limit: int = Query(20, ge=1, le=100),
    before: Optional[str] = Query(
        None, description="ISO format: 2024-01-15T10:30:00"
    ),
):
    try:
        return read_paginate_message(
            session, conversation_id=conversation_id, limit=limit, before=before
        )
    except ValueError as e:
        logger.error(f"Invalid date format: {before}. Error: {e}")
        raise HTTPException(
            status_code=400, detail=f"Invalid value format: {e}"
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Une erreur interne est survenue: {e}"
        )
