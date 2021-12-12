import pytest
from unittest.mock import Mock
from src.database.repositories import PortfolioRepo, AssetRepo
from src.domain.entities.portfolio.services import PortfolioService
from src.domain.entities.portfolio.dto import PortfolioCreateDto, PortfolioUpdateDto
from src.domain.entities.asset.dto import AssetDto
from tests.unit.domain.entities.utils.services.auxiliar_fns import check_create, check_find_all_by_user, check_update, check_delete
from src.domain.exceptions.exceptions import FailedToCreate


class TestAssetService:
    service = PortfolioService

    @pytest.fixture
    def repo(self):
        return Mock(name="portfolio_repo", spec=PortfolioRepo)

    @pytest.fixture
    def asset_repo(self):
        return Mock(name="asset_repo", sepc=AssetRepo)

    @pytest.fixture
    def create_dto(self):
        return PortfolioCreateDto(name="Income Stocks", user_id=99, assets_ids=[101, 201, 301])

    @pytest.fixture
    def update_dto(self):
        return PortfolioCreateDto(name="Income Stocks II", user_id=99, assets_ids=[101, 201, 301, 401, 501])

    def test_create(self, repo, create_dto, asset_repo):
        asset_repo.find_by_ids.return_value = [
            AssetDto(id=101, code="XPTO", name="XPTO", user_id=1),
            AssetDto(id=201, code="XPTO", name="XPTO", user_id=1),
            AssetDto(id=301, code="XPTO", name="XPTO", user_id=1)
        ]
        check_create(self, create_dto, repo=repo, asset_repo=asset_repo)

    def test_create_invalid_assets_ids(self, repo, create_dto, asset_repo):
        asset_repo.find_by_ids.return_value = [
            AssetDto(id=101, code="XPTO", name="XPTO", user_id=1)
        ]
        with pytest.raises(FailedToCreate):
            check_create(self, create_dto, repo=repo, asset_repo=asset_repo)

    def test_find_all_by_user(self, repo, asset_repo):
        check_find_all_by_user(self, repo=repo, asset_repo=asset_repo)

    def test_update(self, repo, update_dto, asset_repo):
        check_update(self, update_dto, repo=repo, asset_repo=asset_repo)

    def test_delete(self, repo, asset_repo):
        check_delete(self, repo=repo, asset_repo=asset_repo)
