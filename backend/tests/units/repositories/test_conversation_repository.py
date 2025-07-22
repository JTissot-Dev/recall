from uuid import UUID
from datetime import datetime
from app.models import Conversation
from app.repositories.conversation_repository import (
    create_conversation,
    read_conversation_by_id,
)
from app.schemas import ConversationCreate


def test_create_conversation(mock_db_session):
    # Arrange
    conversation_create = ConversationCreate(title="Test Conversation")

    # Act
    db_conversation = create_conversation(mock_db_session, conversation_create)

    # Assert
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert db_conversation.title == conversation_create.title
    assert hasattr(db_conversation, "id")
    assert hasattr(db_conversation, "created_at")
    assert hasattr(db_conversation, "updated_at")
    assert db_conversation.messages == []


def test_read_conversation_by_id(mock_db_session):
    # Arrange
    conversation_id = UUID("488098a9-4c50-4786-87be-89628cb1a5b1")
    db_conversation_mock = Conversation(
        id=conversation_id,
        title="Test Conversation",
        messages=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_db_session.get_one.return_value = db_conversation_mock

    # Act
    db_conversation = read_conversation_by_id(mock_db_session, conversation_id)

    # Assert
    mock_db_session.get_one.assert_called_once_with(
        Conversation, conversation_id
    )
    assert db_conversation.id == conversation_id
    assert db_conversation.title == "Test Conversation"
    assert db_conversation.messages == []
    assert hasattr(db_conversation, "created_at")
    assert hasattr(db_conversation, "updated_at")
