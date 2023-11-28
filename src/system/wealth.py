from src.asset import (
    AssetPrototype,
)
from src.mapper import get_class_values


class WEALTH:
    """Static namespace for Wealth assets."""


_assets = get_class_values(WEALTH)


def wealth_list() -> list[AssetPrototype]:
    """Return list of all Wealth Assets."""
    return _assets
