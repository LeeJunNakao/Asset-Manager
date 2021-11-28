from .dto import AssetCreateDto, AssetUpdateDto
from src.database.repositories.asset import AssetRepo


class AssetService:
    def __init__(self, repo: AssetRepo):
        self._repo = repo

    def create(self, dto: AssetCreateDto):
        return self._repo.persist(dto)

    def find_all_by_user(self, user_id: int):
        return self._repo.find_by_user(user_id)

    def update(self, dto: AssetUpdateDto):
        return self._repo.update(dto)

    def delete(self, _id: int, user_id: int):
        return self._repo.delete(_id, user_id)
