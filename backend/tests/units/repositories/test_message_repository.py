from uuid import UUID
from datetime import datetime
from unittest.mock import patch
from app.models import Message
from app.schemas import MessageCreate
from app.repositories.message_repository import (
    create_message,
    read_cursor_paginate_message,
)


def test_create_message(mock_db_session):
    # Arrange
    message_create = MessageCreate(
        content="Hello world",
        role="user",
        conversation_id=UUID("488098a9-4c50-4786-87be-89628cb1a5b1"),
    )

    # Act
    db_message = create_message(mock_db_session, message_create)

    # Assert
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert db_message.content == message_create.content
    assert db_message.role == message_create.role
    assert db_message.conversation_id == message_create.conversation_id
    assert hasattr(db_message, "id")
    assert hasattr(db_message, "created_at")


def test_read_cursor_paginate_message_without_before(mock_db_session):
    #Arrange
    conversation_id = "488098a9-4c50-4786-87be-89628cb1a5b1"
    limit = 20
    before = None

    mock_messages = [
        Message(
            content="Message 1",
            role="user",
            conversation_id=conversation_id,
            created_at=datetime(2024, 1, 15, 10, 0, 0)
        ),
        Message(
            content="Message 2",
            role="assistant",
            conversation_id=conversation_id,
            created_at=datetime(2024, 1, 15, 10, 30, 0)
        )
    ]

    mock_db_session.exec.return_value.all.return_value = mock_messages

    # Act
    messages = read_cursor_paginate_message(
        mock_db_session,
        conversation_id,
        limit=limit,
        before=before
    )

    # Assert
    mock_db_session.exec.assert_called_once()
    assert len(messages) == len(mock_messages)
    assert messages[0].content == "Message 1"
    assert messages[1].content == "Message 2"


def test_read_cursor_paginate_message_with_before(mock_db_session):
    #Arrange
    conversation_id = "488098a9-4c50-4786-87be-89628cb1a5b1"
    limit = 20
    before = datetime(2024, 1, 15, 10, 30, 0)

    mock_messages = [
        Message(
            content="Message 1",
            role="user",
            conversation_id=conversation_id,
            created_at=datetime(2024, 1, 15, 10, 0, 0)
        )
    ]

    mock_db_session.exec.return_value.all.return_value = mock_messages

    # Act
    messages = read_cursor_paginate_message(
        mock_db_session,
        conversation_id,
        limit=limit,
        before=before
    )

    # Assert
    mock_db_session.exec.assert_called_once()
    assert len(messages) == len(mock_messages)
    assert messages[0].content == "Message 1"
    