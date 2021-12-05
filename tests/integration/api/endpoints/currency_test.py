import pytest
from toolz import assoc, dissoc

route = "currency"


class TestCurrencyRoute:
    @pytest.fixture
    def valid_data(self):
        return {
            "code": "USD",
            "name": "Dollar",
            "decimal": 2,
            "user_id": 1
        }

    @pytest.fixture
    def auth_headers(self, create_headers):
        return create_headers(1)

    class TestCreate:
        required_fields = ["code", "name"]

        def test_create_invalid_data(self, client, auth_headers, valid_data):
            for field in self.required_fields:
                data = dissoc(valid_data, field)
                response = client.post(
                    route, json=data, headers=auth_headers)
                assert response.json() == {"details": [
                    {"field": field, "message": "field required"}]}

        def test_create_data(self, client, valid_data, auth_headers):
            response = client.post(
                route, json=valid_data, headers=auth_headers)
            assert response.json() == assoc(valid_data, "id", 1)

    class TestGet:
        @pytest.fixture
        def valid_data(self):
            return [
                {
                    "code": "USD",
                    "name": "Dollar",
                    "decimal": 2,
                    "user_id": 1
                },
                {
                    "code": "BRL",
                    "name": "Real",
                    "decimal": 2,
                    "user_id": 1
                },
                {
                    "code": "IENE",
                    "name": "Iene",
                    "decimal": 0,
                    "user_id": 2
                },
                {
                    "code": "GPB",
                    "name": "British Pound Sterling",
                    "decimal": 2,
                    "user_id": 2
                },
                {
                    "code": "CAD",
                    "name": "Canadian Dollar",
                    "decimal": 2,
                    "user_id": 2
                },

            ]

        @pytest.fixture
        def auth_headers_user_2(self, create_headers):
            return create_headers(2)

        def test_get_all_currencies_of_user(self, client, valid_data, auth_headers, auth_headers_user_2):
            user_id = 1
            expected_currencies = [
                currency for currency in valid_data if currency["user_id"] == user_id
            ]
            for currency in valid_data:
                headers = auth_headers if currency.get(
                    "user_id") == user_id else auth_headers_user_2
                client.post(route, json=currency, headers=headers)

            response = client.get(
                route, headers=auth_headers)
            found_currencies = response.json()

            assert len(found_currencies) == len(expected_currencies)

            for currency in found_currencies:
                assert dissoc(currency, "id") in expected_currencies

    class TestUpdate:
        @pytest.fixture
        def update_data(self):
            return {
                "id": 1,
                "code": "BRl",
                "name": "Real",
                "decimal": 2,
                "user_id": 1
            }

        def test_update_asset(self, client, valid_data, update_data, auth_headers):
            create_response = client.post(
                route, json=valid_data, headers=auth_headers)

            assert create_response.json() == assoc(valid_data, "id", 1)

            update_response = client.put(
                f"{route}/{1}", json=update_data, headers=auth_headers)

            assert update_response.json() == update_data

    class TestDelete:
        def test_delete_asset(self, client, valid_data, auth_headers):
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
