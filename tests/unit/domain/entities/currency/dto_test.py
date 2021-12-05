import pytest
from tests.unit.domain.entities.utils.dto.auxiliar_fns import check_require_at_least_one_field
from src.domain.entities.currency.dto import CurrencyCreateDto, CurrencyDto, CurrencyUpdateDto
from tests.unit.domain.entities.utils.dto.auxliar_cls import DefaultEntityTests


class TestCurrency:
    @pytest.fixture
    def valid_data(self):
        return {
            "id": 100,
            "code": "USD",
            "name": "Dollar",
            "decimal": 2,
            "user_id": 200
        }

    class TestCurrencyCreateDto(DefaultEntityTests):
        required_fields = ["code", "name", "user_id"]
        dto = CurrencyCreateDto
        optional_fields = []

    class TestAssetDto(DefaultEntityTests):
        required_fields = ["id", "code", "name", "decimal", "user_id"]
        dto = CurrencyDto
        optional_fields = []

    class TestUpdateDto(DefaultEntityTests):
        required_fields = ["id", "user_id"]
        dto = CurrencyUpdateDto
        optional_fields = ["code", "name", "decimal"]

        def test_require_at_least_one_field(self, valid_data):
            check_require_at_least_one_field(
                self.dto,
                {
                    "id": valid_data["id"],
                    "user_id": valid_data["user_id"]
                }
            )
