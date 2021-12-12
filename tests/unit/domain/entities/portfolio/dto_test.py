import pytest
from toolz import dissoc
from tests.unit.domain.entities.utils.dto.auxiliar_fns import check_require_at_least_one_field
from src.domain.entities.portfolio.dto import PortfolioCreateDto, PortfolioUpdateDto, PortfolioDto
from tests.unit.domain.entities.utils.dto.auxliar_cls import DefaultEntityTests


class TestPortfolio:
    @pytest.fixture
    def valid_data(self):
        return {
            "id": 100,
            "user_id": 5,
            "name": "Dollar",
            "assets_ids": [1, 2, 3, 4, 5],
        }

    class TestPortfolioCreateDto(DefaultEntityTests):
        required_fields = ["name", "user_id"]
        dto = PortfolioCreateDto
        optional_fields = ["assets_ids"]

    class TestPortfolioDto(DefaultEntityTests):
        required_fields = ["id", "name", "user_id", "assets_ids"]
        dto = PortfolioDto
        optional_fields = []

    class TestUpdateDto(DefaultEntityTests):
        required_fields = ["id", "user_id"]
        dto = PortfolioUpdateDto
        optional_fields = ["name", "assets_ids"]

        def test_require_at_least_one_field(self, valid_data):
            check_require_at_least_one_field(
                self.dto,
                dissoc(valid_data, *self.optional_fields)
            )
