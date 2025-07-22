from uuid import UUID
from datetime import datetime
from unittest.mock import MagicMock, patch
from pytest import fixture
from app.models import Conversation, Message
from app.schemas import ConversationCreate, ChatResponse, ChatMessage
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


@patch('app.services.chat_service.create_message')
def test_process_chat_session(
    mock_create_message, mock_db_session, mock_ollama_provider
):
    # Arrange
    chat_service = ChatService(mock_ollama_provider)

    client_message = "What is the weather today?"
    assistant_response = "The weather is sunny."

    mock_db_conversation = Conversation(
        id=UUID("488098a9-4c50-4786-87be-89628cb1a5b4"),
        title="Test chat session conversation",
        messages=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    mock_user_message = Message(
        id=UUID("488098a9-4c50-4786-87be-89628cb1a5b2"),
        role="user",
        content=client_message,
        conversation_id=UUID("488098a9-4c50-4786-87be-89628cb1a5b4"),
        created_at=datetime.now(),
    )
    mock_assistant_message = Message(
        id=UUID("488098a9-4c50-4786-87be-89628cb1a5b3"),
        role="assistant",
        content=assistant_response,
        conversation_id=UUID("488098a9-4c50-4786-87be-89628cb1a5b4"),
        created_at=datetime.now(),
    )
    mock_create_message.side_effect = [mock_user_message, mock_assistant_message]
    
    mock_message_history = [
            ChatMessage(
                role=mock_user_message.role,
                content=mock_user_message.content
            ),
            ChatMessage(
                role=mock_assistant_message.role,
                content=mock_assistant_message.content
            )
        ]
    
    mock_chat_message = ChatResponse(
        response=assistant_response,
        updated_history=mock_message_history
    )

    mock_ollama_provider.process_chat_message.return_value = mock_chat_message

    # Act
    response = chat_service.process_chat_session(mock_db_session, client_message, mock_db_conversation)

    # Assert
    assert mock_create_message.call_count == 2
    assert response == mock_chat_message
    assert chat_service.chat_history == mock_message_history