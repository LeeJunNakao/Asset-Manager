from typing import Union
from .dto import AssetCreateDto
from src.domain._exceptions.exceptions import FailedToCreate
from src.database.exceptions.exceptions import DatabaseException
from src.database.repositories.asset import AssetRepo


class AssetService:
    def __init__(self, repo: AssetRepo):
        self._repo = repo

    def create(self, dto: AssetCreateDto):
        return self._repo.persist(dto)
