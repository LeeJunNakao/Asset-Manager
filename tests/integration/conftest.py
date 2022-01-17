import pytest
import jwt
import datetime
from src.config import JWT_SECRET
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


def create_token(user_id=1):
    return jwt.encode({"data": {"id": user_id, },  "exp": datetime.datetime.now() + datetime.timedelta(days=1)}, JWT_SECRET, algorithm="HS256")


access_token = create_token()


@pytest.fixture
def create_headers():
    default_user_id = 1
    return lambda user_id: {
        "access_token": access_token if user_id == default_user_id else create_token(user_id),
        "user_id": str(user_id or default_user_id)
    }
