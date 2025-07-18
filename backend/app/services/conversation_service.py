from app.core.database import SessionDep
from app.models import Conversation
from app.schemas import ConversationCreate, ConversationResponse


class ConversationService:
    def __init__(self, session: SessionDep):
        self.session = session

    def read_by_id(self, conversation_id: str) -> ConversationResponse:
        """
        Retrieve a conversation by its ID.
        """
        conversation = self.session.get_one(Conversation, conversation_id)
        return ConversationResponse.model_validate(conversation)

    def create(
        self, conversation_create: ConversationCreate
    ) -> ConversationResponse:
        """
        Create a new conversation in the database.
        """
        conversation = Conversation.model_validate(conversation_create)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return ConversationResponse.model_validate(conversation)
