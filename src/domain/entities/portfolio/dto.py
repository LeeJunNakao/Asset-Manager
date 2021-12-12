from typing import List, Optional
from pydantic import BaseModel, validator
from src.domain.entities.asset.dto import asset_id

portfolio_id = int
portfolio_name = str
portfolio_assets_ids = List[asset_id]
user_id = int


def require_at_least_one_field(fields: List[str], v, values):
    fields_values = [values.get(field) for field in fields]
    not_null_values = [value for value in fields_values if value != None]
    if not v and not len(not_null_values):
        raise ValueError('Must update at least one field')
    return v


class PortfolioDto(BaseModel):
    id: portfolio_id
    user_id: user_id
    name: portfolio_name
    assets_ids: portfolio_assets_ids

    class Config:
        orm_mode = True
        allow_mutation = False


class PortfolioCreateDto(BaseModel):
    name: portfolio_name
    user_id: user_id
    assets_ids: portfolio_assets_ids = []

    class Config:
        orm_mode = True
        allow_mutation = False


class PortfolioUpdateDto(BaseModel):
    id: portfolio_id
    user_id: user_id
    name: Optional[portfolio_name]
    assets_ids: Optional[portfolio_assets_ids]

    class Config:
        orm_mode = True
        allow_mutation = False

    @validator('assets_ids', pre=True, always=True)
    def require_at_least_one_field(cls, v, values):
        return require_at_least_one_field(["name", "assets_ids"], v, values)
