import pytest
from toolz import assoc, dissoc

route = "asset-entry"


class TestAssetRoute:
    @pytest.fixture
    def currency_valid_data(self):
        return {
            "code": "USD",
            "name": "Dollar",
            "decimal": 2,
            "user_id": 1
        }

    @pytest.fixture
    def asset_valid_data(self):
        return {
            "code": "GOOG",
            "name": "Google",
            "user_id": 1
        }

    @pytest.fixture
    def valid_data(self):
        return {
            "id": 111,
            "date": "2020-05-20",
            "asset_id": 1,
            "is_purchase": True,
            "quantity": 100,
            "currency_id": 1,
            "value": 500000,
            "user_id": 1
        }

    @pytest.fixture
    def auth_headers(self, create_headers):
        return create_headers(1)

    @pytest.fixture
    def insert_needed_data(self, client, currency_valid_data, asset_valid_data, auth_headers):
        client.post("currency", json=currency_valid_data,
                    headers=auth_headers)
        client.post("asset", json=asset_valid_data, headers=auth_headers)

    class TestCreate:
        required_fields = ["date", "asset_id",
                           "quantity", "currency_id", "value"]

        def test_create_invalid_data(self, client, auth_headers, valid_data):
            for field in self.required_fields:
                data = dissoc(valid_data, field)
                response = client.post(
                    route, json=data, headers=auth_headers)
                assert response.json() == {"details": [
                    {"field": field, "message": "field required"}]}

        def test_create_data(self, client, valid_data, auth_headers, insert_needed_data):
            response = client.post(
                route, json=valid_data, headers=auth_headers)
            assert response.json() == assoc(valid_data, "id", 1)

    class TestGet:
        @pytest.fixture
        def valid_data(self):
            return [
                {
                    "date": "2020-05-20",
                    "asset_id": 1,
                    "quantity": 100,
                    "currency_id": 1,
                    "is_purchase": True,
                    "value": 500000,
                    "user_id": 1
                },
                {
                    "date": "2020-02-20",
                    "asset_id": 1,
                    "quantity": 600,
                    "currency_id": 1,
                    "is_purchase": True,
                    "value": 700000,
                    "user_id": 1
                },
                {
                    "date": "2020-02-28",
                    "asset_id": 1,
                    "quantity": 100,
                    "is_purchase": False,
                    "currency_id": 1,
                    "value": 700000,
                    "user_id": 1
                },
                {
                    "date": "2020-03-05",
                    "asset_id": 2,
                    "quantity": 200,
                    "is_purchase": True,
                    "currency_id": 1,
                    "value": 80000,
                    "user_id": 1
                },
                {
                    "date": "2020-03-12",
                    "asset_id": 1,
                    "quantity": 300,
                    "is_purchase": False,
                    "currency_id": 1,
                    "value": 62000,
                    "user_id": 2
                },
                {
                    "date": "2020-03-15",
                    "asset_id": 2,
                    "quantity": 150,
                    "is_purchase": False,
                    "currency_id": 1,
                    "value": 77500,
                    "user_id": 2
                },
                {
                    "date": "2020-03-18",
                    "asset_id": 2,
                    "quantity": 300,
                    "is_purchase": True,
                    "currency_id": 1,
                    "value": 12500,
                    "user_id": 2
                },

            ]

        @pytest.fixture
        def auth_headers_user_2(self, create_headers):
            return create_headers(2)

        @pytest.fixture
        def insert_needed_data_2(self, client, currency_valid_data, asset_valid_data, auth_headers_user_2):
            client.post("currency", json=currency_valid_data,
                        headers=auth_headers_user_2)
            client.post("asset", json=asset_valid_data,
                        headers=auth_headers_user_2)

        def test_get_all_asset_entries_of_user(self, client, valid_data, auth_headers, auth_headers_user_2, insert_needed_data, insert_needed_data_2):
            user_id = 1

            assets_entries_asset_1 = [
                asset for asset in valid_data if asset["user_id"] == user_id and asset["asset_id"] == 1
            ]
            assets_entries_asset_2 = [
                asset for asset in valid_data if asset["user_id"] == user_id and asset["asset_id"] == 2
            ]

            for asset in valid_data:
                headers = auth_headers if asset.get(
                    "user_id") == user_id else auth_headers_user_2
                client.post(route, json=asset, headers=headers)

            response = client.get(
                route, headers=auth_headers)
            grouped_assets = response.json()

            assert [dissoc(item, "id")
                    for item in grouped_assets['1']] == assets_entries_asset_1
            assert [dissoc(item, "id")
                    for item in grouped_assets['2']] == assets_entries_asset_2

    class TestUpdate:
        @pytest.fixture
        def update_data(self):
            return {
                "id": 1,
                "date": "2020-10-01",
                "quantity": 100,
                "asset_id": 1,
                "is_purchase": False,
                "value": 10000000,
                "currency_id": 1,
                "user_id": 1
            }

        def test_update_asset(self, client, valid_data, update_data, auth_headers, insert_needed_data):
            create_response = client.post(
                route, json=valid_data, headers=auth_headers)

            assert create_response.json() == assoc(valid_data, "id", 1)

            update_response = client.put(
                f"{route}/{1}", json=update_data, headers=auth_headers)

            assert update_response.json() == update_data

    class TestDelete:
        def test_delete_asset(self, client, valid_data, auth_headers, insert_needed_data):
            create_response = client.post(
                route, json=valid_data, headers=auth_headers)

            assert create_response.json() == assoc(valid_data, "id", 1)
            get_response = client.get(
                route, headers=auth_headers)

            assert len(get_response.json()) == 1

            client.delete(
                f"{route}/{1}", json={"user_id": 1}, headers=auth_headers)

            get_response = client.get(
                route, headers=auth_headers)
            assert len(get_response.json()) == 0
