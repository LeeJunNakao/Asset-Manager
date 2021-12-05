from fastapi import APIRouter, Depends, status, Header, Request
from typing import Optional
from toolz import assoc
from pydantic import BaseModel, validator
from dependency_injector.wiring import inject, Provide
from container import Container
from src.domain.entities.currency.services import CurrencyService as Service
from src.domain.entities.currency.dto import CurrencyCreateDto as CreateDto, CurrencyUpdateDto as UpdateDto

currency_router = APIRouter(prefix="/currency")


class CreateRequestBody(BaseModel):
    name: str
    code: str
    decimal: int = 0


class PutRequestBody(BaseModel):
    code: Optional[str]
    name: Optional[str]
    decimal: Optional[str]

    @validator('decimal', pre=True, always=True)
    def require_at_least_one_field(cls, v, values):
        if not v and not values.get("code") and not values.get("name"):
            raise ValueError('At least one field must be provided to change')
        return v


class DeleteRequestBody(BaseModel):
    user_id: int


@currency_router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create(asset: CreateRequestBody, request: Request, service: Service = Depends(Provide[Container.currency_service])):
    user_id = request.headers.get("user_id")
    dto = CreateDto(**assoc(asset.dict(), "user_id", user_id))
    return service.create(dto)


@currency_router.get("", status_code=status.HTTP_200_OK)
@inject
def index(request: Request, service: Service = Depends(Provide[Container.currency_service])):
    user_id = request.headers.get("user_id")
    items = service.find_all_by_user(user_id)
    return items


@currency_router.put("/{currency_id}", status_code=status.HTTP_200_OK)
@inject
def update(currency_id: int, asset: PutRequestBody, request: Request, service: Service = Depends(Provide[Container.currency_service])):
    user_id = request.headers.get("user_id")
    data = {"id": currency_id, "user_id": user_id, **asset.dict()}

    dto = UpdateDto(**data)
    item = service.update(dto)
    return item


@currency_router.delete("/{asset_id}", status_code=status.HTTP_200_OK)
@inject
def delete(asset_id: int, asset: DeleteRequestBody, service: Service = Depends(Provide[Container.currency_service])):
    service.delete(asset_id, asset.user_id)
    return "deleted"
