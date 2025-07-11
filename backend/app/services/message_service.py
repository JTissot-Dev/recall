from sqlmodel import Session
from app.models import Message
from app.schemas import MessageCreate, MessageResponse


class MessageService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, message_create: MessageCreate) -> MessageResponse:
        """
        Create multiple messages in the database.
        """
        message = Message(
            **message_create.model_dump()
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return MessageResponse(
            **message.model_dump()
        )
