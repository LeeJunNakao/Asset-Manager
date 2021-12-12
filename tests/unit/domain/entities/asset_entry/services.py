import pytest
from unittest.mock import Mock
from src.database.repositories.asset_entry import AssetEntryRepo
from src.domain.entities.asset_entry.services import AssetEntryService
from src.domain.entities.asset_entry.dto import AssetEntryCreateDto, AssetEntryGroupedDto, AssetEntryDto, AssetEntryUpdateDto
from tests.unit.domain.entities.utils.services.auxiliar_fns import check_create, check_find_all_by_user, check_update, check_delete


class TestAssetService:
    service = AssetEntryService

    @pytest.fixture
    def repo(self):
        return Mock(name="currency_repo", spec=AssetEntryRepo)

    @pytest.fixture
    def create_dto(self):
        return AssetEntryCreateDto(date="2020-05-20", asset_id=222, quantity=100, currency_id=333, value=700000, user_id=999)

    @pytest.fixture
    def update_dto(self):
        return AssetEntryUpdateDto(id=1, user_id=99, quantity=300)

    def test_create(self, repo, create_dto):
        check_create(self, create_dto, repo=repo)

    def test_find_all_by_user(self, repo):
        asset_222 = [
            AssetEntryCreateDto(date="2020-05-20", asset_id=222,
                                quantity=100, currency_id=333, value=700000, user_id=999),
            AssetEntryCreateDto(date="2020-02-28", asset_id=222,
                                quantity=100, currency_id=333, value=150000, user_id=999)
        ]
        asset_223 = [
            AssetEntryCreateDto(date="2020-03-05", asset_id=223,
                                quantity=200, currency_id=333, value=80000, user_id=999),
            AssetEntryCreateDto(date="2020-03-12", asset_id=223,
                                quantity=300, currency_id=333, value=62000, user_id=999),
            AssetEntryCreateDto(date="2020-03-15", asset_id=223,
                                quantity=150, currency_id=333, value=77500, user_id=999),
            AssetEntryCreateDto(date="2020-03-18", asset_id=223,
                                quantity=300, currency_id=333, value=12500, user_id=999),
        ]
        repo.find_by_user.return_value = [
            *asset_222, *asset_223
        ]

        service = self.service(repo)
        response = service.find_all_by_user(999)
        assert response == {
            222: [asset.dict() for asset in asset_222],
            223: [asset.dict() for asset in asset_223]
        }

    def test_update(self, repo, update_dto):
        check_update(self, update_dto, repo=repo)

    def test_delete(self, repo):
        check_delete(self, repo=repo)
