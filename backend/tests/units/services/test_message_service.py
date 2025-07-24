from unittest.mock import MagicMock, patch
from datetime import datetime
from app.models import Message
from app.services.message_service import read_paginate_message


@patch("app.services.message_service.read_cursor_paginate_message")
def test_read_paginate_message_without_before(mock_read_cursor_paginate_message, mock_db_session):
    """
    Test reading paginated messages from the database.
    """
    # Arrange
    conversation_id = "488098a9-4c50-4786-87be-89628cb1a5b1"
    limit = 20
    before = None


    mock_messages = [
        Message(
            content="Message 2",
            role="assistant",
            conversation_id=conversation_id,
            created_at=datetime(2024, 1, 15, 10, 30, 0),
        ),
        Message(
            content="Message 1",
            role="user",
            conversation_id=conversation_id,
            created_at=datetime(2024, 1, 15, 10, 0, 0),
        ),
    ]

    mock_read_cursor_paginate_message.return_value = mock_messages

    # Act
    paginate_messages = read_paginate_message(
        mock_db_session, conversation_id, limit=limit, before=before
    )

    # Assert
    mock_read_cursor_paginate_message.assert_called_once()
    assert len(paginate_messages.messages) == len(mock_messages)
    assert paginate_messages.messages[0].content == "Message 1"
    assert paginate_messages.messages[1].content == "Message 2"
    assert paginate_messages.next_cursor == None
    assert paginate_messages.has_next is False


@patch("app.services.message_service.read_cursor_paginate_message")
def test_read_paginate_message_with_before(mock_read_cursor_paginate_message, mock_db_session):
    """
    Test reading paginated messages from the database.
    """
    # Arrange
    conversation_id = "488098a9-4c50-4786-87be-89628cb1a5b1"
    limit = 20
    before = "2024-01-15 10:30:00"


    mock_messages = [
        Message(
            content="Message 1",
            role="user",
            conversation_id=conversation_id,
            created_at=datetime(2024, 1, 15, 10, 0, 0),
        ),
    ]

    mock_read_cursor_paginate_message.return_value = mock_messages

    # Act
    paginate_messages = read_paginate_message(
        mock_db_session, conversation_id, limit=limit, before=before
    )

    # Assert
    mock_read_cursor_paginate_message.assert_called_once()
    assert len(paginate_messages.messages) == 1
    assert paginate_messages.messages[0].content == "Message 1"
    assert paginate_messages.next_cursor == None
    assert paginate_messages.has_next is False