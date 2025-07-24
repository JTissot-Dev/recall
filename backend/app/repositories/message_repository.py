from datetime import datetime
from sqlmodel import Session, select
from typing import Optional
from app.models import Message
from app.schemas import MessageCreate


def create_message(session: Session, message_create: MessageCreate) -> Message:
    message = Message.model_validate(message_create)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def read_cursor_paginate_message(
    session: Session,
    conversation_id: str,
    limit: int = 20,
    before: Optional[datetime] = None,
) -> list[Message]:
    query = select(Message).where(Message.conversation_id == conversation_id)

    if before:
        query = query.where(Message.created_at < before)

    query = query.order_by(Message.created_at.desc()).limit(limit)
    return session.exec(query).all()
