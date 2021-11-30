from fastapi import APIRouter, Depends, status, Header
from typing import Optional
from pydantic import BaseModel, validator
from dependency_injector.wiring import inject, Provide
from container import Container
from src.domain.entities.asset.services import AssetService
from src.domain.entities.asset.dto import AssetCreateDto, AssetUpdateDto

router = APIRouter()


class PutRequestBody(BaseModel):
    user_id: int
    code: Optional[str]
    name: Optional[str]

    @validator('name', pre=True, always=True)
    def require_at_least_one_field(cls, v, values):
        if not v and not values.get("code"):
            raise ValueError('Asset code or name must be provided')
        return v


class DeleteRequestBody(BaseModel):
    user_id: int


@router.post("/asset", status_code=status.HTTP_201_CREATED)
@inject
def create(asset: AssetCreateDto, asset_service: AssetService = Depends(Provide[Container.asset_service])):
    return asset_service.create(asset)


@router.get("/asset", status_code=status.HTTP_200_OK)
@inject
def index(user_id: int, asset_service: AssetService = Depends(Provide[Container.asset_service])):
    items = asset_service.find_all_by_user(user_id)
    return items


@router.put("/asset/{asset_id}", status_code=status.HTTP_200_OK)
@inject
def update(asset_id: int, asset: PutRequestBody, asset_service: AssetService = Depends(Provide[Container.asset_service])):
    data = {"id": asset_id, **asset.dict()}
    dto = AssetUpdateDto(**data)
    item = asset_service.update(dto)
    return item


@router.delete("/asset/{asset_id}", status_code=status.HTTP_200_OK)
@inject
def delete(asset_id: int, asset: DeleteRequestBody, asset_service: AssetService = Depends(Provide[Container.asset_service])):
    asset_service.delete(asset_id, asset.user_id)
    return "deleted"
