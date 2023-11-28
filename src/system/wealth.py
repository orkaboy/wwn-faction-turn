from src.asset import (
    AssetPrototype,
)
from src.mapper import get_class_values

# TIER 1 WEALTH ASSETS
# TIER 2 WEALTH ASSETS
# TIER 3 WEALTH ASSETS
# TIER 4 WEALTH ASSETS
# TIER 5 WEALTH ASSETS
# TIER 6 WEALTH ASSETS
# TIER 7 WEALTH ASSETS
# TIER 8 WEALTH ASSETS


class WEALTH:
    """Static namespace for Wealth assets."""

    # TIER 1 WEALTH ASSETS
    # TIER 2 WEALTH ASSETS
    # TIER 3 WEALTH ASSETS
    # TIER 4 WEALTH ASSETS
    # TIER 5 WEALTH ASSETS
    # TIER 6 WEALTH ASSETS
    # TIER 7 WEALTH ASSETS
    # TIER 8 WEALTH ASSETS


_assets = get_class_values(WEALTH)


def wealth_list() -> list[AssetPrototype]:
    """Return list of all Wealth Assets."""
    return _assets
