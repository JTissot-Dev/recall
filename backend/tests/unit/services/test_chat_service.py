from uuid import UUID
from datetime import datetime
from unittest.mock import MagicMock, patch
from pytest import fixture
from app.models import Conversation, Message
from app.schemas import ConversationCreate
from app.services.chat_service import ChatService
from app.protocols.i_ollama_provider import IOllamaProvider


@fixture
def mock_ollama_provider():
    """Fixture to provide a mock Ollama provider."""
    return MagicMock(spec=IOllamaProvider)

@patch('app.services.chat_service.read_conversation_by_id')
def test_init_chat_session_with_existing_conversation(
    read_conversation_by_id, mock_db_session, mock_ollama_provider
):
    # Arrange
    conversation_id = UUID("488098a9-4c50-4786-87be-89628cb1a5b1")
    mock_message = Message(
        id=UUID("488098a9-4c50-4786-87be-89628cb1a5b1"),
        role="user",
        content="Hello, this is a test message.",
        conversation_id=conversation_id,
        created_at=datetime.now(),
    )
    mock_db_conversation = Conversation(
        id=conversation_id,
        title="Test existing conversation",
        messages=[mock_message],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    read_conversation_by_id.return_value = mock_db_conversation

    chat_service = ChatService(mock_ollama_provider)

    # Act
    conversation = chat_service.init_chat_session(mock_db_session, str(conversation_id))

    # Assert
    read_conversation_by_id.assert_called_once_with(mock_db_session, str(conversation_id))
    assert conversation == mock_db_conversation
    assert chat_service.chat_history[0].role == mock_message.role
    assert chat_service.chat_history[0].content == mock_message.content
    
@patch('app.services.chat_service.create_conversation')
@patch('app.services.chat_service.uuid.uuid4')
def test_init_chat_session_with_new_conversation(
    mock_uuid4, create_conversation, mock_db_session, mock_ollama_provider
):
    # Arrange
    mock_uuid_obj = MagicMock()
    mock_uuid_obj.hex = "abcdef123456789"  
    mock_uuid4.return_value = mock_uuid_obj
    expected_title = "Conversation abcdef"

    mock_create_conversation = ConversationCreate(
        title=expected_title
    )
    mock_db_conversation = Conversation(
        id=UUID("488098a9-4c50-4786-87be-89628cb1a5b2"),
        title=expected_title,
        messages=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    create_conversation.return_value = mock_db_conversation

    chat_service = ChatService(mock_ollama_provider)

    # Act
    conversation = chat_service.init_chat_session(mock_db_session)

    # Assert
    create_conversation.assert_called_once_with(mock_db_session, mock_create_conversation)
    assert conversation == mock_db_conversation
    assert chat_service.chat_history == []
    