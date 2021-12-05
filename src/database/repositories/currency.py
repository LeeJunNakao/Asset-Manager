from typing import List

from src.domain.entities.currency.dto import CurrencyCreateDto, CurrencyDto, CurrencyUpdateDto
from src.database.model.currency import Curency as Model
from src.database.config import Session
from src.database.repositories.utils.fns import persist, find_by_user, update, delete


class CurrencyRepo:
    def __init__(self, session: Session):
        self._session = session
        self._entity = "currency"
        self.model = Model
        self.base_model = CurrencyDto

    def persist(self, dto: CurrencyCreateDto) -> CurrencyDto:
        return persist(self, dto)

    def find_by_user(self, user_id: int) -> List[CurrencyDto]:
        return find_by_user(self, user_id)

    def update(self, dto: CurrencyUpdateDto) -> CurrencyDto:
        return update(self, dto)

    def delete(self, _id: int, user_id: int) -> None:
        return delete(self, _id, user_id)
