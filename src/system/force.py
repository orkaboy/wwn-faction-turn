from typing import Self

from src.asset import (
    AssetPrototype,
    AssetRequirement,
    AssetStats,
    AssetStrings,
    AssetType,
)
from src.mapper import get_class_values


# TIER 1 FORCE ASSETS
class FearfulIntimidation(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Fearful Intimidation",
                ident="c_fearful_intimidation",
                damage_formula="None",
                counter_formula="1d4 damage",
                rules="Judicious exercises of force have intimidated the locals, making them reluctant to cooperate with any group that stands opposed to the faction.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=2,
            ),
            stats=AssetStats(
                max_hp=4,
            ),
        )


class LocalGuard(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Local Guard",
                ident="c_local_guard",
                damage_formula="F v. F/1d3+1 damage",
                counter_formula="1d4+1 damage",
                rules="Judicious exercises of force have intimidated the locals, making them reluctant to cooperate with any group that stands opposed to the faction.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=3,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
            ),
        )


# TIER 2 FORCE ASSETS
# TIER 3 FORCE ASSETS
# TIER 4 FORCE ASSETS
# TIER 5 FORCE ASSETS
# TIER 6 FORCE ASSETS
# TIER 7 FORCE ASSETS
# TIER 8 FORCE ASSETS


class FORCE:
    """Static namespace for Force assets."""

    # TIER 1 FORCE ASSETS
    FearfulIntimidation = FearfulIntimidation()
    # TIER 2 FORCE ASSETS
    # TIER 3 FORCE ASSETS
    # TIER 4 FORCE ASSETS
    # TIER 5 FORCE ASSETS
    # TIER 6 FORCE ASSETS
    # TIER 7 FORCE ASSETS
    # TIER 8 FORCE ASSETS


_assets = get_class_values(FORCE)


def force_list() -> list[AssetPrototype]:
    """Return list of all Force Assets."""
    return _assets
