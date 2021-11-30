import pytest
from toolz import assoc, dissoc

from src.api.endpoints import delete


class TestAssetRoute:
    @pytest.fixture
    def valid_data(self):
        return {
            "code": "GOOG",
            "name": "Google",
            "user_id": 1
        }

    class TestCreate:
        required_fields = ["code", "name", "user_id"]

        def test_create_invalid_data(self, client, valid_data):
            for field in self.required_fields:
                data = dissoc(valid_data, field)
                response = client.post("asset", json=data)
                assert response.json() == {"details": [
                    {"field": field, "message": "field required"}]}

        def test_create_data(self, client, valid_data):
            response = client.post("asset", json=valid_data)
            assert response.json() == assoc(valid_data, "id", 1)

    class TestGet:
        @pytest.fixture
        def valid_data(self):
            return [
                {
                    "code": "GOOG",
                    "name": "Google",
                    "user_id": 1
                },
                {
                    "code": "AAPL",
                    "name": "Apple",
                    "user_id": 1
                },
                {
                    "code": "AMZN",
                    "name": "Amazon",
                    "user_id": 2
                },
                {
                    "code": "TSLA",
                    "name": "Tesla",
                    "user_id": 2
                },
                {
                    "code": "NFLX",
                    "name": "Netflix",
                    "user_id": 2
                },

            ]

        def test_get_all_assets_of_user(self, client, valid_data):
            user_id = 1
            expected_assets = [
                asset for asset in valid_data if asset["user_id"] == user_id
            ]
            for asset in valid_data:
                client.post("asset", json=asset)

            response = client.get(f"asset?user_id={user_id}")
            found_assets = response.json()

            assert len(found_assets) == len(expected_assets)

            for asset in found_assets:
                assert asset in found_assets

    class TestUpdate:
        @pytest.fixture
        def update_data(self):
            return {
                "id": 1,
                "code": "AMZN",
                "name": "Amazon",
                "user_id": 1
            }

        def test_update_asset(self, client, valid_data, update_data):
            create_response = client.post("asset", json=valid_data)

            assert create_response.json() == assoc(valid_data, "id", 1)

            update_response = client.put(f"asset/{1}", json=update_data)

            assert update_response.json() == update_data

    class TestDelete:
        def test_delete_asset(self, client, valid_data):
            create_response = client.post("asset", json=valid_data)

            assert create_response.json() == assoc(valid_data, "id", 1)
            get_response = client.get(f"asset?user_id={1}")

            assert len(get_response.json()) == 1

            client.delete(f"asset/{1}", json={"user_id": 1})

            get_response = client.get(f"asset?user_id={1}")
            assert len(get_response.json()) == 0
