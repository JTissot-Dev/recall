from unittest.mock import Mock
import pytest
from app.main import app
from app.core.database import get_session


mock_session = Mock()


def override_get_session():
    try:
        yield mock_session
    finally:
        pass


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture
def mock_db_session():
    """
    Fixture to provide a mock database session.
    """
    return mock_session
