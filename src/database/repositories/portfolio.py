from typing import List

from src.domain.entities.portfolio.dto import PortfolioCreateDto, PortfolioUpdateDto, PortfolioDto
from src.database.model.portfolio import Portfolio as Model
from src.database.config import Session
from src.database.repositories.utils.fns import persist, find_by_user, update, delete, find_by
from src.database.exceptions.exceptions import UniqueViolationException


class PortfolioRepo:
    def __init__(self, session: Session):
        self._session = session
        self._entity = "portfolio"
        self.model = Model
        self.base_model = PortfolioDto

    def persist(self, dto: PortfolioCreateDto) -> PortfolioDto:
        item = find_by(self, dto.user_id, name=dto.name)
        if len(item):
            raise UniqueViolationException(self._entity)
        return persist(self, dto)

    def find_by_user(self, user_id: int) -> List[PortfolioDto]:
        return find_by_user(self, user_id)

    def update(self, dto: PortfolioUpdateDto) -> PortfolioDto:
        return update(self, dto)

    def delete(self, _id: int, user_id: int) -> None:
        return delete(self, _id, user_id)
