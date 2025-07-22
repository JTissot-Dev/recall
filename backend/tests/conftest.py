from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.core.database import get_session


mock_session = MagicMock()


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


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)


@pytest.fixture
def client(test_client):
    # Configuration pour intégration
    yield test_client


@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset all mocks before each test."""
    mock_session.reset_mock()
