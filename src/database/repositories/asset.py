from src.domain.Asset.dto import AssetCreateDto, AssetDto
from src.database.model.asset import Asset as Model
from src.database.config import Session
from src.database.exceptions.adapter import db_exc_adapter
from src.domain._exceptions.exceptions import FailedToCreate
from src.database.exceptions.exceptions import UniqueViolationException
from sqlalchemy.sql.expression import select


class AssetRepo:
    def __init__(self, session: Session):
        self._session = session

    def persist(self, dto: AssetCreateDto):
        item = self._session.query(Model).filter(
            Model.code == dto.code).all()
        if len(item):
            raise UniqueViolationException("asset")
        try:
            data = Model(**dto.dict())
            self._session.add(data)
            self._session.commit()
            self._session.refresh(data)
        except Exception:
            self._session.rollback()
            raise FailedToCreate("asset")
        finally:
            self._session.close()

        return AssetDto.from_orm(data)
