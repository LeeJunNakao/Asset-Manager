from typing import List

from src.domain.entities.asset.dto import AssetCreateDto, AssetDto, AssetUpdateDto
from src.database.model.asset import Asset as Model
from src.database.config import Session
from src.database.repositories.utils.fns import persist, find_by_user, update, delete


class AssetRepo:
    def __init__(self, session: Session):
        self._session = session
        self._entity = "asset"
        self.model = Model
        self.base_model = AssetDto

    def persist(self, dto: AssetCreateDto) -> AssetDto:
        return persist(self, dto)

    def find_by_user(self, user_id: int) -> List[AssetDto]:
        return find_by_user(self, user_id)

    def update(self, dto: AssetUpdateDto) -> AssetDto:
        return update(self, dto)

    def delete(self, _id: int, user_id: int) -> None:
        return delete(self, _id, user_id)
