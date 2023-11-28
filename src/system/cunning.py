from typing import Self

from src.asset import (
    AssetPrototype,
    AssetRequirement,
    AssetStats,
    AssetStrings,
    AssetType,
    MagicLevel,
)
from src.mapper import get_class_values
from src.system.qualities import QUALITY


# TIER 1 CUNNING ASSETS
class Informers(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Informers",
                ident="c_informers",
                damage_formula="C v. C/Special",
                counter_formula="None",
                rules="As a free action, once per turn, the faction can spend 1 Treasure and have the Informers look for Stealthed Assets. To do so, the Informers pick a faction and make a Cunning vs. Cunning Attack on them. No counterattack damage is taken if they fail, but if they succeed, all Stealthed Assets of that faction within one move of the Informers are revealed",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=2,
            ),
            stats=AssetStats(
                max_hp=3,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle],
            ),
        )


class PettySeers(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Petty Seers",
                ident="c_petty_seers",
                damage_formula="None",
                counter_formula="1d6 damage",
                rules="A cadre of skilled fortune-tellers and minor oracles have been enlisted by the faction to foresee perils and allow swift counterattacks.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=2,
                magic_level=MagicLevel.MEDIUM,
            ),
            stats=AssetStats(
                max_hp=2,
                qualities=[QUALITY.Subtle],
            ),
        )


class CUNNING:
    """Static namespace for Cunning asset prototypes."""

    # TIER 1 CUNNING ASSETS
    Informers = Informers()
    PettySeers = PettySeers()

    # TIER 2 CUNNING ASSETS
    # TIER 3 CUNNING ASSETS
    # TIER 4 CUNNING ASSETS
    # TIER 5 CUNNING ASSETS
    # TIER 6 CUNNING ASSETS
    # TIER 7 CUNNING ASSETS
    # TIER 8 CUNNING ASSETS


_assets = get_class_values(CUNNING)


def cunning_list() -> list[AssetPrototype]:
    """Return list of all Cunning Assets."""
    return _assets
