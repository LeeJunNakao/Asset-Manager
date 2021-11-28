from dependency_injector import containers, providers
from src.domain.entities.asset.services import AssetService
from src.database.repositories.asset import AssetRepo
from src.database.config import Session


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["src.api.endpoints"])

    session = providers.Factory(Session)
    asset_repo = providers.Factory(AssetRepo, session=session)
    asset_service = providers.Factory(
        AssetService,
        repo=asset_repo
    )
