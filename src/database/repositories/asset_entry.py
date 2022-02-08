from typing import List

from src.domain.entities.asset_entry.dto import AssetEntryCreateDto, AssetEntryDto, AssetEntryUpdateDto
from src.database.model.asset_entry import AssetEntry as Model
from src.database.config import Session
from src.database.repositories.utils.fns import find_by_user, update, delete
from src.domain.exceptions.exceptions import FailedToCreate


class AssetEntryRepo:
    def __init__(self, session: Session):
        self._session = session
        self._entity = "Asset Entry"
        self.model = Model
        self.base_model = AssetEntryDto

    def persist(self, dto: AssetEntryCreateDto) -> AssetEntryDto:
        try:
            data = self.model(**dto.dict())
            self._session.add(data)
            self._session.commit()
            self._session.refresh(data)
            return self.base_model.from_orm(data)
        except Exception as err:
            self._session.rollback()
            raise FailedToCreate(self._entity, "Failed to create")
        finally:
            self._session.close()

    def find_by_user(self, user_id: int) -> List[AssetEntryDto]:
        return find_by_user(self, user_id)

    def update(self, dto: AssetEntryUpdateDto) -> AssetEntryDto:
        return update(self, dto)

    def delete(self, _id: int, user_id: int) -> None:
        return delete(self, _id, user_id)
