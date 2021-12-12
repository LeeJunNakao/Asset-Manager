from typing import List

from .dto import PortfolioCreateDto, PortfolioDto, PortfolioUpdateDto
from src.database.repositories import PortfolioRepo, AssetRepo
from src.domain.exceptions.exceptions import FailedToCreate


class PortfolioService:
    def __init__(self, repo: PortfolioRepo, asset_repo: AssetRepo):
        self._repo = repo
        self._asset_repo = asset_repo
        self._entity = "portfolio"

    def create(self, dto: PortfolioCreateDto) -> PortfolioDto:
        assets = self._asset_repo.find_by_ids(dto.user_id, dto.assets_ids)
        assets_ids = list(
            map(lambda asset: asset.id, assets)
        )
        invalid_assets_ids = list(
            filter(
                lambda id_: id_ not in assets_ids,
                dto.assets_ids
            )
        )

        if(len(invalid_assets_ids)):
            ids_string = ", ".join([str(id_) for id_ in invalid_assets_ids])
            raise FailedToCreate(
                self._entity, f"Invalid asset ids: {ids_string}")

        return self._repo.persist(dto)

    def find_all_by_user(self, user_id: int) -> List[PortfolioDto]:
        return self._repo.find_by_user(user_id)

    def update(self, dto: PortfolioUpdateDto) -> PortfolioDto:
        return self._repo.update(dto)

    def delete(self, _id: int, user_id: int) -> None:
        return self._repo.delete(_id, user_id)
