from uuid import UUID
from datetime import datetime
import json
from unittest.mock import patch, MagicMock
from app.models import Conversation, Message
from app.schemas import ChatResponse, ChatMessage


@patch("app.websocket.routes.chat.ChatService")
def test_websocket_chat_endpoint(MockChatService, mock_db_session, client):
    # Arrange
    client_message = "Hello !"
    assistant_response = "Hi, how can i help you today ?"

    ## Mock the ChatService instance
    mock_chat_service = MagicMock()
    MockChatService.return_value = mock_chat_service

    mock_conversation = Conversation(
        id=UUID("488098a9-4c50-4786-87be-89628cb1a5b8"),
        title="Test Conversation",
        messages=[],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_chat_service.init_chat_session.return_value = mock_conversation

    mock_user_chat_message = ChatMessage(
        role="user",
        content=client_message,
    )
    mock_assistant_chat_message = ChatMessage(
        role="assistant",
        content=assistant_response,
    )

    mock_chat_service.process_chat_session.return_value = ChatResponse(
        response="Hi, how can i help you today ?",
        updated_history=[mock_user_chat_message, mock_assistant_chat_message],
    )

    # Act
    with client.websocket_connect("/ws/chat") as websocket:
        websocket.send_text(client_message)
        response_text = websocket.receive_text()
        response = json.loads(response_text)

        # Assert
        mock_chat_service.init_chat_session.assert_called_once_with(
            mock_db_session, None
        )
        mock_chat_service.process_chat_session.assert_called_once_with(
            mock_db_session, client_message, mock_conversation
        )
        assert response["type"] == "message"
        assert response["content"] == assistant_response
        assert "timestamp" in response


@patch("app.websocket.routes.chat.ChatService")
def test_websocket_chat_endpoint_with_client_id(
    MockChatService, mock_db_session, client
):
    # Arrange
    client_message = "Hello !"
    assistant_response = "Hi, how can i help you today ?"

    ## Mock the ChatService instance
    mock_chat_service = MagicMock()
    MockChatService.return_value = mock_chat_service

    mock_existing_user_message = Message(
        id=UUID("488098a9-4c50-4786-87be-89628cb1a5b2"),
        role="user",
        content="previous user msg",
        conversation_id=UUID("488098a9-4c50-4786-87be-89628cb1a5b4"),
        created_at=datetime.now(),
    )
    mock_existing_assistant_message = Message(
        id=UUID("488098a9-4c50-4786-87be-89628cb1a5b3"),
        role="assistant",
        content="previous assistant message",
        conversation_id=UUID("488098a9-4c50-4786-87be-89628cb1a5b4"),
        created_at=datetime.now(),
    )

    mock_conversation = Conversation(
        id=UUID("488098a9-4c50-4786-87be-89628cb1a5b9"),
        title="Test existing conversation",
        messages=[mock_existing_user_message, mock_existing_assistant_message],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    mock_chat_service.init_chat_session.return_value = mock_conversation

    mock_user_chat_message = ChatMessage(
        role="user",
        content=client_message,
    )
    mock_assistant_chat_message = ChatMessage(
        role="assistant",
        content=assistant_response,
    )

    mock_chat_service.process_chat_session.return_value = ChatResponse(
        response="Hi, how can i help you today ?",
        updated_history=[
            ChatMessage(
                role=mock_existing_user_message.role,
                content=mock_existing_user_message.content,
            ),
            ChatMessage(
                role=mock_existing_assistant_message.role,
                content=mock_existing_assistant_message.content,
            ),
            mock_user_chat_message,
            mock_assistant_chat_message,
        ],
    )

    # Act
    with client.websocket_connect(
        "/ws/chat?conversation_id=488098a9-4c50-4786-87be-89628cb1a5b9"
    ) as websocket:
        websocket.send_text(client_message)
        response_text = websocket.receive_text()
        response = json.loads(response_text)

        # Assert
        mock_chat_service.init_chat_session.assert_called_once_with(
            mock_db_session, "488098a9-4c50-4786-87be-89628cb1a5b9"
        )
        mock_chat_service.process_chat_session.assert_called_once_with(
            mock_db_session, client_message, mock_conversation
        )
        assert response["type"] == "message"
        assert response["content"] == assistant_response
        assert "timestamp" in response
