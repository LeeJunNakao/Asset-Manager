from typing import List

from src.domain.entities.asset.dto import AssetCreateDto, AssetDto, AssetUpdateDto, asset_id
from src.database.model.asset import Asset as Model
from src.database.config import Session
from src.database.repositories.utils.fns import persist, find_by_user, update, delete, find_by, find_in
from src.database.exceptions.exceptions import UniqueViolationException


class AssetRepo:
    def __init__(self, session: Session):
        self._session = session
        self._entity = "asset"
        self.model = Model
        self.base_model = AssetDto

    def persist(self, dto: AssetCreateDto) -> AssetDto:
        item = find_by(self, dto.user_id, code=dto.code)
        if len(item):
            raise UniqueViolationException(self._entity)
        return persist(self, dto)

    def find_by_ids(self, user_id: int, ids: List[asset_id]):
        return find_in(self, user_id, "id", ids)

    def find_by_user(self, user_id: int) -> List[AssetDto]:
        return find_by_user(self, user_id)

    def update(self, dto: AssetUpdateDto) -> AssetDto:
        return update(self, dto)

    def delete(self, _id: int, user_id: int) -> None:
        return delete(self, _id, user_id)
