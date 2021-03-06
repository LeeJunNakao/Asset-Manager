import pytest
from src.domain.entities.asset.dto import AssetCreateDto, AssetDto, AssetUpdateDto
from tests.unit.domain.entities.utils.dto.auxiliar_fns import check_require_at_least_one_field
from tests.unit.domain.entities.utils.dto.auxliar_cls import DefaultEntityTests


class TestAsset:
    @pytest.fixture
    def valid_data(self):
        return {
            "id": 100,
            "code": "GOOG",
            "name": "Google",
            "user_id": 200
        }

    class TestAssetCreateDto(DefaultEntityTests):
        required_fields = ["code", "name", "user_id"]
        dto = AssetCreateDto
        optional_fields = []

    class TestAssetDto(DefaultEntityTests):
        required_fields = ["id", "code", "name", "user_id"]
        dto = AssetDto
        optional_fields = []

    class TestUpdateDto(DefaultEntityTests):
        required_fields = ["id", "user_id"]
        dto = AssetUpdateDto
        optional_fields = ["code", "name"]

        def test_require_at_least_one_field(self, valid_data):
            check_require_at_least_one_field(
                self.dto,
                {
                    "id": valid_data["id"],
                    "user_id": valid_data["user_id"]
                }
            )
