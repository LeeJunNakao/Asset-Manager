from fastapi import APIRouter, Depends, status, Header, Request
from typing import Optional
from toolz import assoc
from pydantic import BaseModel, validator
from dependency_injector.wiring import inject, Provide
import yfinance as yf
from container import Container
from src.domain.entities.asset.services import AssetService
from src.domain.entities.asset.dto import AssetCreateDto, AssetUpdateDto

asset_router = APIRouter(prefix="/asset")


class CreateRequestBody(BaseModel):
    name: str
    code: str


class PutRequestBody(BaseModel):
    code: Optional[str]
    name: Optional[str]

    @validator('name', pre=True, always=True)
    def require_at_least_one_field(cls, v, values):
        if not v and not values.get("code"):
            raise ValueError('Asset code or name must be provided')
        return v


class DeleteRequestBody(BaseModel):
    user_id: int


@asset_router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create(asset: CreateRequestBody, request: Request, asset_service: AssetService = Depends(Provide[Container.asset_service])):
    user_id = request.headers.get("user_id")
    dto = AssetCreateDto(**assoc(asset.dict(), "user_id", user_id))
    return asset_service.create(dto)


@asset_router.get("", status_code=status.HTTP_200_OK)
@inject
def index(request: Request, asset_service: AssetService = Depends(Provide[Container.asset_service])):
    user_id = request.headers.get("user_id")
    items = asset_service.find_all_by_user(user_id)
    return items


@asset_router.put("/{asset_id}", status_code=status.HTTP_200_OK)
@inject
def update(asset_id: int, asset: PutRequestBody, request: Request, asset_service: AssetService = Depends(Provide[Container.asset_service])):
    user_id = request.headers.get("user_id")
    data = {"id": asset_id, "user_id": user_id, **asset.dict()}

    dto = AssetUpdateDto(**data)
    item = asset_service.update(dto)
    return item


@asset_router.delete("/{asset_id}", status_code=status.HTTP_200_OK)
@inject
def delete(asset_id: int, request: Request,  asset_service: AssetService = Depends(Provide[Container.asset_service])):
    user_id = request.headers.get("user_id")
    asset_service.delete(asset_id, user_id)
    return "deleted"


@asset_router.get("/price/{asset_code}", status_code=status.HTTP_200_OK)
@inject
def index(request: Request, asset_code: str, asset_service: AssetService = Depends(Provide[Container.asset_service])):
    msft = yf.Ticker(asset_code)
    history = msft.history(period="max")
    price = history.iloc[-1].at['Close']
    date = history.iloc[-1].name.date()

    return {"price": round(price, 2), "date": date}
