from sqlmodel import Session
from app.models import Conversation
from app.schemas import ConversationCreate, ConversationResponse


class ConversationService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, conversation_create: ConversationCreate) -> ConversationResponse:
        """
        Create a new conversation in the database.
        """
        conversation = Conversation(
            **conversation_create.model_dump()
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return ConversationResponse(
            **conversation.model_dump()
        )
