import pytest
from unittest.mock import Mock
from src.database.repositories.asset import AssetRepo
from src.domain.entities.asset.services import AssetService
from src.domain.entities.asset.dto import AssetCreateDto, AssetUpdateDto
from tests.unit.domain.entities.utils.services.auxiliar_fns import check_create, check_find_all_by_user, check_update, check_delete


class TestAssetService:
    service = AssetService

    @pytest.fixture
    def repo(self):
        return Mock(name="asset_repo", spec=AssetRepo)

    @pytest.fixture
    def create_dto(self):
        return AssetCreateDto(code="GOOG", name="Google", user_id=99)

    @pytest.fixture
    def update_dto(self):
        return AssetUpdateDto(id=1, user_id=99, name="Yahoo")

    def test_create(self, repo, create_dto):
        check_create(self,  create_dto, repo=repo)

    def test_find_all_by_user(self, repo):
        check_find_all_by_user(self, repo=repo)

    def test_update(self, repo, update_dto):
        check_update(self, update_dto, repo=repo)

    def test_delete(self, repo):
        check_delete(self, repo=repo)
