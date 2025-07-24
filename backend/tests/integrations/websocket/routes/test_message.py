from unittest.mock import patch, MagicMock
from uuid import UUID
from datetime import datetime
from app.schemas.message import (
    MessageResponse, MessagesPaginateResponse
)


@patch("app.api.routes.message.read_paginate_message")
def test_read_messages(mock_read_paginate_message, mock_db_session, client):
    """
    Test reading messages from the database.
    """
    # Arrange
    conversation_id = "488098a9-4c50-4786-87be-89628cb1a5e5"
    limit = 20

    mock_messages = [
        MessageResponse(
            id=UUID("488098a9-4c50-4786-87be-89628cb1a5b1"),
            content="Message 1",
            role="user",
            created_at=datetime(2024, 1, 15, 10, 0, 0),
        ),
        MessageResponse(
            id=UUID("488098a9-4c50-4786-87be-89628cb1a5b2"),
            content="Message 2",
            role="assistant",
            created_at=datetime(2024, 1, 15, 10, 30, 0),
        ),
    ]

    mock_read_paginate_message.return_value = MessagesPaginateResponse(
        messages=mock_messages,
        next_cursor=None,
        has_next=False
    )

    # Act
    response = client.get(
        f"api/messages?conversation_id={conversation_id}&limit={limit}"
    )
    data = response.json()

    # Assert
    mock_read_paginate_message.assert_called_once_with(
        mock_db_session, conversation_id=conversation_id, limit=limit, before=None
    )
    assert response.status_code == 200
    assert len(data["messages"]) == len(mock_messages)
    assert data["messages"][0]["content"] == "Message 1"
    assert data["messages"][1]["content"] == "Message 2"