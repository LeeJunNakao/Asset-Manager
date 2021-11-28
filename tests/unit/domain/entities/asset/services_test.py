import pytest
from unittest.mock import Mock
from src.database.repositories.asset import AssetRepo
from src.domain.entities.asset.services import AssetService
from src.domain.entities.asset.dto import AssetCreateDto, AssetUpdateDto


class TestAssetService:
    @pytest.fixture
    def repo(self):
        return Mock(name="asset_repo", spec=AssetRepo)

    @pytest.fixture
    def asset_create_dto(self):
        return AssetCreateDto(code="GOOG", name="Google", user_id=99)

    @pytest.fixture
    def asset_update_dto(self):
        return AssetUpdateDto(id=1, user_id=99, name="Yahoo")

    def test_create(self, repo, asset_create_dto):
        expected_return = "persisted"
        repo.persist.return_value = expected_return

        service = AssetService(repo)
        result = service.create(asset_create_dto)

        assert result == expected_return

    def test_find_all_by_user(self, repo):
        expected_return = "all found"
        repo.find_by_user.return_value = expected_return

        service = AssetService(repo)
        result = service.find_all_by_user(user_id=1)

        assert result == expected_return

    def test_update(self, repo, asset_update_dto):
        expected_return = "updated"
        repo.update.return_value = expected_return

        service = AssetService(repo)
        result = service.update(asset_update_dto)

        assert result == expected_return

    def test_delete(self, repo):
        expected_return = "deleted"
        repo.delete.return_value = expected_return

        service = AssetService(repo)
        result = service.delete(_id=1, user_id=99)

        assert result == expected_return
