from typing import Optional
from sqlmodel import Session
from app.core.utils import parse_datetime
from app.repositories.message_repository import read_cursor_paginate_message
from app.schemas import MessagesPaginateResponse


def read_paginate_message(
    session: Session,
    conversation_id: str,
    limit: int = 20,
    before: Optional[str] = None,
) -> MessagesPaginateResponse:

    before_datetime = parse_datetime(before) if before else None
    messages = read_cursor_paginate_message(
        session, conversation_id, limit, before_datetime
    )
    messages.reverse()
    has_next = len(messages) == limit
    next_cursor = messages[-1].created_at if has_next else None
    return MessagesPaginateResponse(
        messages=messages, next_cursor=next_cursor, has_next=has_next
    )
