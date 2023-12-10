from enum import Enum, auto
from functools import total_ordering
from typing import Self

from src.quality import Quality


class AssetType(Enum):
    """AssetType enumeration."""

    CUNNING = auto()
    FORCE = auto()
    WEALTH = auto()


@total_ordering
class MagicLevel(Enum):
    """MagicLevel enumeration."""

    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def __lt__(self: Self, other: Self) -> bool:
        return self.value < other.value


class AssetRequirement:
    def __init__(
        self: Self, tier: int, cost: int, magic_level: MagicLevel = MagicLevel.NONE
    ) -> None:
        """Initialize AssetRequirement object."""
        self.tier = tier
        self.cost = cost
        self.magic_level = magic_level


class AssetStats:
    def __init__(
        self: Self,
        max_hp: int,
        upkeep: int = 0,
        atk_type: AssetType = None,
        def_type: AssetType = None,
        qualities: list[Quality] = None,
    ) -> None:
        """Initialize AssetStats object."""
        self.max_hp = max_hp
        self.upkeep = upkeep
        self.atk_type = atk_type
        self.def_type = def_type
        if qualities:
            self.qualities = qualities
        else:
            self.qualities = []


class AssetStrings:
    def __init__(
        self: Self,
        name: str,
        ident: str,
        rules: str,
        damage_formula: str = "None",
        counter_formula: str = "None",
    ) -> None:
        """Initialize AssetStrings object."""
        self.name: str = name
        self.id: str = ident
        self.rules: str = rules
        self.damage_formula: str = damage_formula
        self.counter_formula: str = counter_formula


class AssetPrototype:
    def __init__(
        self: Self,
        asset_type: AssetType,
        # Static descriptions
        strings: AssetStrings,
        # Stats (shared between all instances)
        requirements: AssetRequirement,
        stats: AssetStats,
    ) -> None:
        """Initialize AssetPrototype object."""
        self.type = asset_type
        # Static descriptions
        self.strings = strings
        # Stats (shared between all instances)
        self.requirements = requirements
        self.stats = stats

    def roll_damage(self: Self) -> int:
        """Need to override with asset damage formula."""
        return 0

    def roll_counter(self: Self) -> int:
        """Need to override with asset counter formula."""
        return 0

    def upkeep(self: Self) -> int:
        """Calculate upkeep for a given asset."""
        return self.stats.upkeep

    def __repr__(self: Self) -> str:
        return self.strings.name
