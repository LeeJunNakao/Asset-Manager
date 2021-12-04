import pytest
from freezegun import freeze_time
import datetime


class TestAuthenticatioMiddlewares:
    def test_invalid_token(self, client):
        response = client.get(
            "asset", headers={"user_id": "1", "access_token": "invalid_token"})

        assert response.json() == {"details": "Credentials invalid"}

    @freeze_time(datetime.datetime.now() + datetime.timedelta(days=1, seconds=1))
    def test_expired_token(self, client, create_headers):
        response = client.get(
            "asset", headers=create_headers(1))

        assert response.json() == {"details": "Credentials invalid"}
