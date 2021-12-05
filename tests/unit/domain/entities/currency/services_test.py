import pytest
from unittest.mock import Mock
from src.database.repositories.currency import CurrencyRepo
from src.domain.entities.currency.services import CurrencyService
from src.domain.entities.currency.dto import CurrencyCreateDto, CurrencyUpdateDto
from tests.unit.domain.entities.utils.services.auxiliar_fns import check_create, check_find_all_by_user, check_update, check_delete


class TestAssetService:
    service = CurrencyService

    @pytest.fixture
    def repo(self):
        return Mock(name="currency_repo", spec=CurrencyRepo)

    @pytest.fixture
    def create_dto(self):
        return CurrencyCreateDto(code="USD", name="Dolar", user_id=99)

    @pytest.fixture
    def update_dto(self):
        return CurrencyUpdateDto(id=1, user_id=99, name="Dollar")

    def test_create(self, repo, create_dto):
        check_create(self, repo, create_dto)

    def test_find_all_by_user(self, repo):
        check_find_all_by_user(self, repo)

    def test_update(self, repo, update_dto):
        check_update(self, repo, update_dto)

    def test_delete(self, repo):
        check_delete(self, repo)
