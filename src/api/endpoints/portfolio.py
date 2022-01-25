from fastapi import APIRouter, Depends, status, Request
from typing import Optional
from toolz import assoc
from pydantic import BaseModel, validator
from dependency_injector.wiring import inject, Provide
from container import Container
from src.domain.entities.portfolio.services import PortfolioService as Service
from src.domain.entities.portfolio.dto import PortfolioCreateDto as CreateDto, PortfolioUpdateDto as UpdateDto, portfolio_name, portfolio_assets_ids

portfolio_router = APIRouter(prefix="/portfolio")


class CreateRequestBody(BaseModel):
    name: portfolio_name
    assets_ids: portfolio_assets_ids = []


class PutRequestBody(BaseModel):
    name: Optional[portfolio_name]
    assets_ids: Optional[portfolio_assets_ids]


class DeleteRequestBody(BaseModel):
    user_id: int


@portfolio_router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create(portfolio: CreateRequestBody, request: Request, service: Service = Depends(Provide[Container.portfolio_service])):
    user_id = request.headers.get("user_id")
    dto = CreateDto(**assoc(portfolio.dict(), "user_id", user_id))
    return service.create(dto)


@portfolio_router.get("", status_code=status.HTTP_200_OK)
@inject
def index(request: Request, service: Service = Depends(Provide[Container.portfolio_service])):
    user_id = request.headers.get("user_id")
    items = service.find_all_by_user(user_id)
    return items


@portfolio_router.put("/{portfolio_id}", status_code=status.HTTP_200_OK)
@inject
def update(portfolio_id: int, portfolio: PutRequestBody, request: Request, service: Service = Depends(Provide[Container.portfolio_service])):
    user_id = request.headers.get("user_id")
    data = {"id": portfolio_id, "user_id": user_id, **portfolio.dict()}

    dto = UpdateDto(**data)
    item = service.update(dto)
    return item


@portfolio_router.delete("/{portfolio_id}", status_code=status.HTTP_200_OK)
@inject
def delete(portfolio_id: int, request: Request, service: Service = Depends(Provide[Container.portfolio_service])):
    user_id = request.headers.get("user_id")
    service.delete(portfolio_id, user_id)
    return "deleted"
