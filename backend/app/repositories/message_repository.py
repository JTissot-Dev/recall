from sqlmodel import Session
from app.models import Message
from app.schemas import MessageCreate


def create_message(session: Session, message_create: MessageCreate) -> Message:
    message = Message.model_validate(message_create)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message
