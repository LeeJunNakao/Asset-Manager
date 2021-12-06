from typing import List

from .dto import AssetEntryCreateDto, AssetEntryDto, AssetEntryUpdateDto, AssetEntryGroupedDto
from src.database.repositories.asset_entry import AssetEntryRepo


class AssetEntryService:
    def __init__(self, repo: AssetEntryRepo):
        self._repo = repo

    def create(self, dto: AssetEntryCreateDto) -> AssetEntryDto:
        return self._repo.persist(dto)

    def find_all_by_user(self, user_id: int) -> List[AssetEntryGroupedDto]:
        asset_entries = self._repo.find_by_user(user_id)
        grouped_entries = {}

        for asset_entry in asset_entries:
            entries = grouped_entries.get(asset_entry.asset_id)
            if not entries:
                grouped_entries.update({asset_entry.asset_id: [asset_entry]})
            else:
                entries.append(asset_entry)

        return grouped_entries

    def update(self, dto: AssetEntryUpdateDto) -> AssetEntryDto:
        return self._repo.update(dto)

    def delete(self, _id: int, user_id: int) -> None:
        return self._repo.delete(_id, user_id)
