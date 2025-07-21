from sqlmodel import Session
from app.models import Conversation
from app.schemas import ConversationCreate


def read_conversation_by_id(
    session: Session, conversation_id: str
) -> Conversation:
    return session.get_one(Conversation, conversation_id)


def create_conversation(
    session: Session, conversation_create: ConversationCreate
) -> Conversation:
    conversation = Conversation.model_validate(conversation_create)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation
