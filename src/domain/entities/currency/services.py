from typing import List

from .dto import CurrencyCreateDto, CurrencyUpdateDto, CurrencyDto
from src.database.repositories.currency import CurrencyRepo


class CurrencyService:
    def __init__(self, repo: CurrencyRepo):
        self._repo = repo

    def create(self, dto: CurrencyCreateDto) -> CurrencyDto:
        return self._repo.persist(dto)

    def find_all_by_user(self, user_id: int) -> List[CurrencyDto]:
        return self._repo.find_by_user(user_id)

    def update(self, dto: CurrencyUpdateDto) -> CurrencyDto:
        return self._repo.update(dto)

    def delete(self, _id: int, user_id: int) -> None:
        return self._repo.delete(_id, user_id)
