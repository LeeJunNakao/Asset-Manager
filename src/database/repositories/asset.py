from typing import List

from src.domain.entities.asset.dto import AssetCreateDto, AssetDto, AssetUpdateDto
from src.database.model.asset import Asset as Model
from src.database.config import Session
from src.domain.exceptions.exceptions import FailedToCreate, FailedToFind, FailedToUpdate, FailedToDelete
from src.database.exceptions.exceptions import UniqueViolationException, InexistentItem


class AssetRepo:
    def __init__(self, session: Session):
        self._session = session
        self._entity = "asset"

    def persist(self, dto: AssetCreateDto) -> AssetDto:
        item = self._session.query(Model).filter(
            Model.code == dto.code).filter(Model.user_id == dto.user_id).all()
        if len(item):
            raise UniqueViolationException(self._entity)
        try:
            data = Model(**dto.dict())
            self._session.add(data)
            self._session.commit()
            self._session.refresh(data)
            return AssetDto.from_orm(data)
        except Exception:
            self._session.rollback()
            raise FailedToCreate(self._entity)
        finally:
            self._session.close()

    def find_by_user(self, user_id: int) -> List[AssetDto]:
        try:
            items = self._session.query(Model).filter(
                Model.user_id == user_id).all()
            return [AssetDto.from_orm(item) for item in items]
        except Exception:
            raise FailedToFind(self._entity)
        finally:
            self._session.close()

    def update(self, dto: AssetUpdateDto) -> AssetDto:
        asset = self._session.query(Model).filter(
            Model.id == dto.id).first()
        if not asset:
            raise InexistentItem(self._entity)
        try:
            for key, value in dto.dict(exclude_none=True).items():
                setattr(asset, key, value)
            self._session.commit()
            return AssetDto.from_orm(asset)
        except Exception:
            self._session.rollback()
            raise FailedToUpdate(self._entity)
        finally:
            self._session.close()

    def delete(self, _id: int, user_id: int) -> None:
        asset = self._session.query(Model).filter(
            Model.id == _id
        ).filter(
            Model.user_id == user_id
        ).first()
        if not asset:
            raise InexistentItem(self._entity)
        try:
            self._session.delete(asset)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise FailedToDelete(self._entity)
        finally:
            self._session.close()
