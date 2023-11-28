from enum import Enum, auto
from typing import Self

from imgui_bundle import imgui

from src.quality import Quality


class AssetType(Enum):
    """AssetType enumeration."""

    CUNNING = auto()
    FORCE = auto()
    WEALTH = auto()


class MagicLevel(Enum):
    """MagicLevel enumeration."""

    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


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
        damage_formula: str,
        counter_formula: str,
        rules: str,
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


class Asset:
    def __init__(
        self: Self,
        prototype: AssetPrototype,
        owner: str,
    ) -> None:
        """Instantiate Asset object."""
        # Variable stats
        self.desc: str = ""
        self.owner = owner
        self.uuid: str = ""
        self.prototype = prototype
        self.hp: int = prototype.stats.max_hp
        self.qualities: list[Quality] = []
        if prototype.stats.qualities:
            self.qualities.extend(prototype.stats.qualities)

    def render(self: Self, idx: str) -> None:
        """Render asset in GUI."""
        imgui.text(self.prototype.strings.name)
        # TODO(orkaboy): Multiline?
        _, self.desc = imgui.input_text(label=f"Description##{idx}", str=self.desc)
        _, self.hp = imgui.input_int(label=f"HP##{idx}", v=self.hp)
        imgui.same_line()
        imgui.text(f"/{self.prototype.stats.max_hp}")
        imgui.text_wrapped(f"Damage: {self.prototype.strings.damage_formula}")
        imgui.text_wrapped(f"Counter: {self.prototype.strings.counter_formula}")
        imgui.text_wrapped(self.prototype.strings.rules)
        if self.prototype.stats.upkeep:
            imgui.text(f"Upkeep: {self.prototype.stats.upkeep}")
        # Qualities
        imgui.text("Qualities:")
        if len(self.qualities) > 0:
            rm_quality = -1
            for q_idx, quality in enumerate(self.qualities):
                imgui.same_line()
                imgui.text(quality.name)
                imgui.same_line()
                if imgui.button(f"X##{idx}_{q_idx}", size=imgui.ImVec2(16, 16)):
                    rm_quality = q_idx
            if rm_quality >= 0:
                self.qualities.pop(rm_quality)
        # TODO(orkaboy): Button to add new Quality to Asset.
