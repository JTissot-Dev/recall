from sqlmodel import Session
from app.models import Message

class MessageService:
    def __init__(self, session: Session):
        self.session = session
    
    def create_many(self, messages: list[Message]) -> list[Message]:
        """
        Create multiple messages in the database.
        """
        self.session.add_all(messages)
        self.session.commit()
        self.session.refresh(messages)
        return messages