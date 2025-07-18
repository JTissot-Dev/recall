from app.core.database import SessionDep
from app.models import Message
from app.schemas import MessageCreate, MessageResponse


class MessageService:
    def __init__(self, session: SessionDep):
        self.session = session

    def create(self, message_create: MessageCreate) -> MessageResponse:
        """
        Create message in the database.
        """
        message = Message.model_validate(message_create)
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return MessageResponse.model_validate(message)
