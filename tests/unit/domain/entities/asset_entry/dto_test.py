import pytest
from toolz import assoc
from pydantic import ValidationError
from src.domain.entities.asset_entry.dto import AssetEntryCreateDto, AssetEntryDto, AssetEntryUpdateDto
from tests.unit.domain.entities.utils.dto.auxiliar_fns import check_require_at_least_one_field
from tests.unit.domain.entities.utils.dto.auxliar_cls import DefaultEntityTests


class TestAsset:
    @pytest.fixture
    def valid_data(self):
        return {
            "id": 111,
            "date": "2020-05-20",
            "asset_id": 222,
            "is_purchase": True,
            "quantity": 100,
            "currency_id": 333,
            "value": 500000,
            "user_id": 999
        }

    class TestAssetEntryCreateDto(DefaultEntityTests):
        required_fields = [
            "date", "asset_id", "is_purchase", "quantity", "currency_id", "value", "user_id"
        ]
        dto = AssetEntryCreateDto
        optional_fields = []

        def test_invalid_date(self, valid_data):
            invalid_dates = ["2021-02-31", "2000-30-12",
                             1248598, False, None, "", "someday"]
            for invalid_date in invalid_dates:
                with pytest.raises(ValidationError):
                    self.dto(**assoc(valid_data, "date", invalid_date))

    class TestAssetDto(DefaultEntityTests):
        required_fields = [
            "id", "date", "asset_id", "is_purchase", "quantity", "currency_id", "value", "user_id"
        ]
        dto = AssetEntryDto
        optional_fields = []

    class TestUpdateDto(DefaultEntityTests):
        required_fields = [
            "id", "user_id"
        ]
        dto = AssetEntryUpdateDto
        optional_fields = [
            "date", "quantity", "is_purchase", "currency_id", "value"
        ]

        def test_require_at_least_one_field(self, valid_data):
            check_require_at_least_one_field(
                self.dto,
                {
                    "id": valid_data["id"],
                    "user_id": valid_data["user_id"]
                }
            )
