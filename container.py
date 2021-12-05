from dependency_injector import containers, providers
from src.domain.entities.asset.services import AssetService
from src.domain.entities.currency.services import CurrencyService
from src.database.repositories import AssetRepo, CurrencyRepo

from src.database.config import Session


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["src.api.endpoints.asset", "src.api.endpoints.currency"])

    session = providers.Factory(Session)
    asset_repo = providers.Factory(AssetRepo, session=session)
    currency_repo = providers.Factory(CurrencyRepo, session=session)
    asset_service = providers.Factory(
        AssetService,
        repo=asset_repo
    )
    currency_service = providers.Factory(
        CurrencyService,
        repo=currency_repo
    )
