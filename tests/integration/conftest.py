import pytest
from fastapi.testclient import TestClient
from src.api.server import create_app
from tests.integration.utils.database import truncate_database


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture(autouse=True)
def database(app):
    truncate_database()
