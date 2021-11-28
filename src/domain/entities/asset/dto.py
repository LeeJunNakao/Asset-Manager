from pydantic import BaseModel, validator
from typing import Optional

asset_id = int
asset_code = str
asset_name = str
asset_user_id = int


class AssetCreateDto(BaseModel):
    code: asset_code
    name: asset_name
    user_id: asset_user_id

    class Config:
        orm_mode = True
        allow_mutation = False


class AssetDto(BaseModel):
    id: asset_id
    code: asset_code
    name: asset_name
    user_id: asset_user_id

    class Config:
        orm_mode = True
        allow_mutation = False


class AssetUpdateDto(BaseModel):
    id: asset_id
    user_id: asset_user_id
    code: Optional[asset_code]
    name: Optional[asset_name]

    class Config:
        orm_mode = True
        allow_mutation = False

    @validator('name', pre=True, always=True)
    def require_at_least_one_field(cls, v, values):
        if not v and not values.get("code"):
            raise ValueError('Asset code or name must be provided')
