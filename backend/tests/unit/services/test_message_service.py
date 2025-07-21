import sys
from unittest.mock import Mock
from app.schemas import MessageCreate

# mock_database_module = Mock()
# mock_database_module.SessionDep = Mock()
# sys.modules['app.core.database'] = Mock()

# Maintenant l'import fonctionne
from app.repositories.message_repository import create_message


def test_create_message(mock_db_session):
    # Arrange
    message_create = MessageCreate(
        content="Hello world",
        role="user",
        conversation_id="488098a9-4c50-4786-87be-89628cb1a5b1"
    )

    # Act
    response = create_message(mock_db_session, message_create)

    # Assert
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert response.content == message_create.content
    assert response.role == message_create.role
