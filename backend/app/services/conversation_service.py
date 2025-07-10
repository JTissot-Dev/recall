from sqlmodel import Session
from app.models import Conversation

class ConversationService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, conversation: Conversation) -> Conversation:
        """
        Create a new conversation in the database.
        """
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation