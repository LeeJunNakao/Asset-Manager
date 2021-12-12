import pytest
from toolz import assoc, dissoc

route = "portfolio"


class TestPortfolioRoute:
    @pytest.fixture
    def currency_valid_data(self):
        return [{
            "code": "USD",
            "name": "Dollar",
            "decimal": 2,
            "user_id": 1
        }]

    @pytest.fixture
    def asset_valid_data(self):
        return [
            {
                "code": "GOOG",
                "name": "Google",
                "user_id": 1
            },
            {
                "code": "AMZN",
                "name": "Amazon",
                "user_id": 1
            },
        ]

    @pytest.fixture
    def valid_data(self):
        return {
            "name": "Valuation Stocks",
            "assets_ids": [1, 2],
            "user_id": 1
        }

    @pytest.fixture
    def auth_headers(self, create_headers):
        return create_headers(1)

    @pytest.fixture
    def necessary_data(self, insert_datas, currency_valid_data, asset_valid_data, auth_headers):
        insert_datas(
            [
                (currency_valid_data, "currency"),
                (asset_valid_data, "asset")
            ],
            auth_headers
        )

    @pytest.fixture
    def insert_datas(self, client):
        def fn(datas, auth_headers):
            for (data, data_route) in datas:
                for item in data:
                    client.post(
                        data_route,
                        json=item,
                        headers=auth_headers
                    )
        return fn

    class TestCreate:
        required_fields = ["name"]

        def test_create_invalid_data(self, client, auth_headers, valid_data):
            for field in self.required_fields:
                data = dissoc(valid_data, field)
                response = client.post(
                    route, json=data, headers=auth_headers
                )
                assert response.json() == {"details": [
                    {"field": field, "message": "field required"}]}

        def test_create_data(self, client, valid_data, auth_headers, necessary_data):
            response = client.post(
                route, json=valid_data, headers=auth_headers
            )
            assert response.json() == assoc(valid_data, "id", 1)

        def test_create_invalid_assets_ids(self, client, valid_data, auth_headers, necessary_data):
            invalid_assets_ids = [4, 5, 6]
            response = client.post(
                route, json=assoc(valid_data, "assets_ids", invalid_assets_ids), headers=auth_headers
            )
            assets_ids_string = ", ".join(
                [str(id_) for id_ in invalid_assets_ids]
            )
            assert response.json() == {
                "details": f"Invalid asset ids: {assets_ids_string}",
                "entity": "portfolio"
            }

    class TestGet:
        @pytest.fixture
        def valid_data(self):
            return [
                {
                    "name": "Valuation Stocks",
                    "assets_ids": [1, 2],
                    "user_id": 1
                },
                {
                    "name": "Incoming Stocks",
                    "assets_ids": [1],
                    "user_id": 1
                },
                {
                    "name": "Small caps",
                    "assets_ids": [1, 2],
                    "user_id": 1
                },
            ]

        @pytest.fixture
        def valid_data_user_2(self):
            return [
                {
                    "name": "Blue chips",
                    "assets_ids": [1, 2, 3],
                    "user_id": 2
                },
                {
                    "name": "Misterious Portfolio",
                    "assets_ids": [1],
                    "user_id": 2
                },
            ]

        @pytest.fixture
        def asset_valid_data_user_2(self):
            return [
                {
                    "code": "AAPL",
                    "name": "Apple",
                    "user_id": 2
                },
                {
                    "code": "MSFT",
                    "name": "Microsoft",
                    "user_id": 2
                },
                {
                    "code": "GOOG",
                    "name": "Google",
                    "user_id": 2
                },
                {
                    "code": "TSLA",
                    "name": "TEsla",
                    "user_id": 2
                },
            ]

        @pytest.fixture
        def auth_headers_user_2(self, create_headers):
            return create_headers(2)

        @pytest.fixture
        def necessary_data_user_2(self, currency_valid_data, asset_valid_data_user_2, auth_headers_user_2, insert_datas):
            insert_datas(
                [
                    (currency_valid_data, "currency"),
                    (asset_valid_data_user_2, "asset")
                ],
                auth_headers_user_2
            )

        def test_get_all_asset_entries_of_user(self, client, valid_data, valid_data_user_2, auth_headers, auth_headers_user_2, necessary_data, necessary_data_user_2):
            user_id = 1

            for portfolio in valid_data:
                client.post(route, json=portfolio, headers=auth_headers)

            for portfolio in valid_data_user_2:
                client.post(route, json=portfolio, headers=auth_headers_user_2)

            response = client.get(
                route, headers=auth_headers)
            response_user_2 = client.get(
                route, headers=auth_headers_user_2)

            response_data = response.json()
            response_data_user_2 = response_user_2.json()

            assert len(response_data) != len(response_data_user_2)
            assert len(response_data) == len(valid_data)

            for item in response_data:
                assert dissoc(item, "id") in valid_data
                assert dissoc(item, "id") not in valid_data_user_2

            for item in response_data_user_2:
                assert dissoc(item, "id") in valid_data_user_2
                assert dissoc(item, "id") not in valid_data

    class TestUpdate:
        @pytest.fixture
        def update_data(self):
            return {
                "id": 1,
                "name": "Renamed Stocks",
                "assets_ids": [1],
                "user_id": 1
            }

        def test_update_asset(self, client, valid_data, update_data, auth_headers, necessary_data):
            create_response = client.post(
                route, json=valid_data, headers=auth_headers)

            assert create_response.json() == assoc(valid_data, "id", 1)

            update_response = client.put(
                f"{route}/{1}", json=update_data, headers=auth_headers)

            assert update_response.json() == update_data

    class TestDelete:
        def test_delete_asset(self, client, valid_data, auth_headers, necessary_data):
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
