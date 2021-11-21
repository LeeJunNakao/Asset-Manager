from pydantic import BaseModel


class AssetDto(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        orm_mode = True
        allow_mutation = False


class AssetCreateDto(BaseModel):
    code: str
    name: str

    class Config:
        orm_mode = True
        allow_mutation = False
