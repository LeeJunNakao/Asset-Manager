import pytest
from toolz import assoc


class TestAssetRoute:
    @pytest.fixture
    def valid_data(self):
        return {
            "code": "GOOG",
            "name": "Google",
            "user_id": 1
        }

    class TestCreate:
        def test_create_invalid_data(self, client, valid_data):
            response = client.post("asset", json=valid_data)
            assert response.json() == assoc(valid_data, "id", 1)
