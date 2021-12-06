from .asset import asset_router
from .currency import currency_router
from .asset_entry import asset_entry_router


def register_routes(app):
    routes = [asset_router, currency_router, asset_entry_router]

    for route in routes:
        app.include_router(route)
