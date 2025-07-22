from uuid import UUID
from app.schemas import MessageCreate
from app.repositories.message_repository import create_message


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
