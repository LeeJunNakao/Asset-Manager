from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide
from container import Container
from src.domain.Asset.services import AssetService
from src.domain.Asset.dto import AssetCreateDto

router = APIRouter()


@router.post("/asset", status_code=status.HTTP_201_CREATED)
@inject
def create(asset: AssetCreateDto, asset_service: AssetService = Depends(Provide[Container.asset_service])):
    return asset_service.create(asset)
