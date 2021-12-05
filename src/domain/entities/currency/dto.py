from typing import Optional
from pydantic import BaseModel, validator

currency_id = int
currency_name = str
currency_code = str
currency_decimal = int
user_id = int


class CurrencyCreateDto(BaseModel):
    code: currency_code
    name: currency_name
    decimal: currency_decimal = 0
    user_id: user_id

    class Config:
        orm_mode = True
        allow_mutation = False


class CurrencyDto(BaseModel):
    id: currency_id
    code: currency_code
    name: currency_name
    decimal: currency_decimal
    user_id: user_id

    class Config:
        orm_mode = True
        allow_mutation = False


class CurrencyUpdateDto(BaseModel):
    id: currency_id
    user_id: user_id
    code: Optional[currency_code]
    name: Optional[currency_name]
    decimal: Optional[currency_decimal]

    class Config:
        orm_mode = True
        allow_mutation = False

    @validator('decimal', pre=True, always=True)
    def require_at_least_one_field(cls, v, values):
        if not v and not values.get("code") and not values.get("name"):
            raise ValueError('At least one field must be provided')
        return v
