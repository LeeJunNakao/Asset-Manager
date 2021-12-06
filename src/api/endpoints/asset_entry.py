from fastapi import APIRouter, Depends, status, Header, Request
from typing import Optional
from toolz import assoc
from pydantic import BaseModel, validator
from dependency_injector.wiring import inject, Provide
from container import Container
from src.domain.entities.asset_entry.services import AssetEntryService
from src.domain.entities.asset_entry.dto import AssetEntryCreateDto, AssetEntryUpdateDto, entry_date, entry_asset_id, entry_user_id, entry_quantity, entry_currency_id, entry_value

asset_entry_router = APIRouter(prefix="/asset-entry")


class CreateRequestBody(BaseModel):
    date: entry_date
    asset_id: entry_asset_id
    quantity: entry_quantity
    currency_id: entry_currency_id
    value: entry_value


class PutRequestBody(BaseModel):
    date: Optional[entry_date]
    quantity: Optional[entry_quantity]
    currency_id: Optional[entry_currency_id]
    value: Optional[entry_value]


class DeleteRequestBody(BaseModel):
    user_id: int


@asset_entry_router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create(asset: CreateRequestBody, request: Request, service: AssetEntryService = Depends(Provide[Container.asset_entry_service])):
    user_id = request.headers.get("user_id")
    dto = AssetEntryCreateDto(**assoc(asset.dict(), "user_id", user_id))
    return service.create(dto)


@asset_entry_router.get("", status_code=status.HTTP_200_OK)
@inject
def index(request: Request, service: AssetEntryService = Depends(Provide[Container.asset_entry_service])):
    user_id = request.headers.get("user_id")
    items = service.find_all_by_user(user_id)
    return items


@asset_entry_router.put("/{asset_id}", status_code=status.HTTP_200_OK)
@inject
def update(asset_id: int, asset: PutRequestBody, request: Request, service: AssetEntryService = Depends(Provide[Container.asset_entry_service])):
    user_id = request.headers.get("user_id")
    data = {"id": asset_id, "user_id": user_id, **asset.dict()}

    dto = AssetEntryUpdateDto(**data)
    item = service.update(dto)
    return item


@asset_entry_router.delete("/{asset_id}", status_code=status.HTTP_200_OK)
@inject
def delete(asset_id: int, asset: DeleteRequestBody, service: AssetEntryService = Depends(Provide[Container.asset_entry_service])):
    service.delete(asset_id, asset.user_id)
    return "deleted"
