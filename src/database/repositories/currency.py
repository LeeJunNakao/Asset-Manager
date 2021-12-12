from typing import List

from src.domain.entities.currency.dto import CurrencyCreateDto, CurrencyDto, CurrencyUpdateDto
from src.database.model.currency import Curency as Model
from src.database.config import Session
from src.database.repositories.utils.fns import persist, find_by_user, update, delete
from src.database.exceptions.exceptions import UniqueViolationException


class CurrencyRepo:
    def __init__(self, session: Session):
        self._session = session
        self._entity = "currency"
        self.model = Model
        self.base_model = CurrencyDto

    def persist(self, dto: CurrencyCreateDto) -> CurrencyDto:
        item = self._session.query(self.model).filter(
            self.model.code == dto.code
        ).filter(
            self.model.user_id == dto.user_id
        ).all()
        if len(item):
            raise UniqueViolationException(self._entity)
        return persist(self, dto)

    def find_by_user(self, user_id: int) -> List[CurrencyDto]:
        return find_by_user(self, user_id)

    def update(self, dto: CurrencyUpdateDto) -> CurrencyDto:
        return update(self, dto)

    def delete(self, _id: int, user_id: int) -> None:
        return delete(self, _id, user_id)
