from typing import Any, List
from sqlalchemy import and_
from toolz import assoc

from src.database.exceptions.exceptions import InexistentItem
from src.domain.exceptions.exceptions import FailedToCreate, FailedToFind, FailedToUpdate, FailedToDelete


def persist(self, dto):
    try:
        data = self.model(**dto.dict())
        self._session.add(data)
        self._session.commit()
        self._session.refresh(data)
        return self.base_model.from_orm(data)
    except Exception:
        self._session.rollback()
        raise FailedToCreate(self._entity)
    finally:
        self._session.close()


def find_by(self, user_id: int, **kwargs):
    try:
        items = self._session.query(self.model).filter(
            and_(
                *[getattr(self.model, key) == kwargs[key] for key in kwargs]
            )
        ).filter(self.model.user_id == user_id).all()
        return [self.base_model.from_orm(item) for item in items]
    except Exception:
        self._session.rollback()
        raise FailedToFind(self._entity)
    finally:
        self._session.close()


def find_in(self, user_id: int, field: str, values: List[Any]):
    try:
        items = self._session.query(self.model).filter(self.model.user_id == user_id).filter(
            *[getattr(self.model, field).in_(values)]
        ).all()
        return [self.base_model.from_orm(item) for item in items]
    except Exception:
        self._session.rollback()
        raise FailedToFind(self._entity)
    finally:
        self._session.close()


def find_by_user(self, user_id: int):
    try:
        items = self._session.query(
            self.model
        ).filter(
            self.model.user_id == user_id
        ).all()
        return [self.base_model.from_orm(item) for item in items]
    except Exception:
        raise FailedToFind(self._entity)
    finally:
        self._session.close()


def update(self, dto):
    item = self._session.query(
        self.model
    ).filter(
        self.model.id == dto.id).first()
    if not item:
        raise InexistentItem(self._entity)
    try:
        for key, value in dto.dict(exclude_none=True).items():
            setattr(item, key, value)
        self._session.commit()
        return self.base_model.from_orm(item)
    except Exception:
        self._session.rollback()
        raise FailedToUpdate(self._entity)
    finally:
        self._session.close()


def delete(self, _id: int, user_id: int) -> None:
    item = self._session.query(self.model).filter(
        self.model.id == _id
    ).filter(
        self.model.user_id == user_id
    ).first()
    if not item:
        raise InexistentItem(self._entity)
    try:
        self._session.delete(item)
        self._session.commit()
    except Exception:
        self._session.rollback()
        raise FailedToDelete(self._entity)
    finally:
        self._session.close()
