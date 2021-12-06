from pydantic import BaseModel, validator
from datetime import date
from typing import Dict, List, Optional
from re import match
from src.database.model.asset import Base

from src.domain.entities.asset.dto import asset_id
from src.domain.entities.currency.dto import currency_id

entry_id = int
entry_date = str
entry_asset_id = asset_id
entry_quantity = int
entry_currency_id = currency_id
entry_value = int
entry_user_id = int


def check_date_format(v):
    pattern = r"\d{4}-\d{1,2}-\d{1,2}"

    if match(pattern, v):
        try:
            (year, month, day) = v.split("-")
            date(year=int(year), month=int(month), day=int(day))
            return v
        except Exception:
            raise ValueError('Invalid date format')
    else:
        raise ValueError('Invalid date format')


class AssetEntryCreateDto(BaseModel):
    date: entry_date
    asset_id: entry_asset_id
    user_id: entry_user_id
    quantity: entry_quantity
    currency_id: entry_currency_id
    value: entry_value

    class Config:
        orm_mode = True
        allow_mutation = False

    @validator('date', pre=True, always=True)
    def check_date_format(cls, v, values):
        return check_date_format(v)


class AssetEntryDto(BaseModel):
    id: entry_id
    date: entry_date
    asset_id: entry_asset_id
    quantity: entry_quantity
    currency_id: entry_currency_id
    value: entry_value
    user_id: entry_user_id

    class Config:
        orm_mode = True
        allow_mutation = False


class AssetEntryUpdateDto(BaseModel):
    id: entry_id
    user_id: entry_user_id
    date: Optional[entry_date]
    quantity: Optional[entry_quantity]
    currency_id: Optional[entry_currency_id]
    value: Optional[entry_value]

    class Config:
        orm_mode = True
        allow_mutation = False

    @validator('date', pre=True, always=True)
    def check_date_format(cls, v, values):
        if not v:
            return v
        return check_date_format(v)

    @validator('value', pre=True, always=True)
    def require_at_least_one_field(cls, v, values):
        if not v and not values.get("date") and not values.get("quantity") and not values.get("currency_id") and not values.get("value"):
            raise ValueError('At least one field to updated must be provided')
        return v


AssetEntryGroupedDto = Dict[entry_asset_id, List[AssetEntryDto]]
