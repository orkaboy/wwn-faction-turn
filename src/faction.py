from enum import Enum
from random import randint
from typing import Self

from imgui_bundle import imgui

from src.asset import Asset, AssetType
from src.layout_helper import LayoutHelper
from src.tag import Tag


class MagicLevel(Enum):
    """Initialize MagicLevel object."""

    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Faction:
    MAX_ATTRIBUTE: int = 8

    # Cost in exp to raise an attribute level
    # Also doubles for HP value of an attribute at faction creation
    ATTRIBUTE_COST: dict[int, int] = {
        1: 1,  # Note, attribute level 1 never needs to be bought (just for hp value)
        2: 2,
        3: 4,
        4: 6,
        5: 9,
        6: 12,
        7: 16,
        8: 20,
    }

    def __init__(
        self: Self, ident: str, name: str, cunning: int, force: int, wealth: int, magic: MagicLevel
    ) -> None:
        """Initialize Faction object."""
        self.name = name
        self.desc: str = ""
        self.id: str = ident
        # Main faction attributes
        self.cunning: int = cunning
        self.force: int = force
        self.wealth: int = wealth
        self.magic: MagicLevel = magic
        # Secondary faction attributes
        self.exp: int = 0
        self.treasure: int = 0
        self.hp: int = self.max_hp()
        # Asset tracking
        self.assets: list[Asset] = []
        # Tags tracking
        self.tags: list[Tag] = []

    def max_hp(self: Self) -> int:
        """Calculate faction max hp."""
        hp = 0
        hp += Faction.ATTRIBUTE_COST[self.cunning]
        hp += Faction.ATTRIBUTE_COST[self.force]
        hp += Faction.ATTRIBUTE_COST[self.wealth]
        return hp

    def roll_initiative(self: Self) -> int:
        """At the start of every faction turn, each faction rolls 1d8 for initiative, the highest rolls going first."""  # noqa: E501
        return randint(1, 8)

    def roll_cunning(self: Self) -> int:
        """Make a 1d10 Cunning roll."""
        return randint(1, 10) + self.cunning

    def roll_force(self: Self) -> int:
        """Make a 1d10 Force roll."""
        return randint(1, 10) + self.force

    def roll_wealth(self: Self) -> int:
        """Make a 1d10 Wealth roll."""
        return randint(1, 10) + self.wealth

    def treasure_gain(self: Self) -> int:
        """The faction earns Treasure equal to half their Wealth, plus a quarter of their combined Force and Cunning, the total being rounded up."""  # noqa: D401, E501
        gain = self.wealth / 2 + (self.force + self.cunning) / 4
        return gain.__ceil__()

    def assets_by_type(self: Self, asset_type: AssetType) -> list[Asset]:
        """Return a list of all asset of a certain type."""
        return [asset for asset in self.assets if asset.type == asset_type]

    def asset_upkeep(self: Self) -> int:
        """The faction must pay any upkeep required by their individual Asset costs."""  # noqa: D401
        upkeep = 0
        # Sum up cost of assets
        for asset in self.assets:
            upkeep += asset.upkeep
        return upkeep

    def asset_excess(self: Self, asset_type: AssetType) -> int:
        """[...] or by the cost of having too many Assets for their attributes."""
        # Get appropriate attribute
        limit = 0
        match asset_type:
            case AssetType.CUNNING:
                limit = self.cunning
            case AssetType.FORCE:
                limit = self.force
            case AssetType.WEALTH:
                limit = self.wealth
        # Count assets
        nr_assets = len(self.assets_by_type(asset_type))
        # Account for excess assets
        if nr_assets > limit:
            return nr_assets - limit
        return 0

    def render(self: Self, idx: int) -> None:
        """Render faction in GUI."""
        header_open, visible = imgui.collapsing_header(f"{self.name}##{idx}", True, flags=32)
        if header_open and visible:
            _, self.name = imgui.input_text(label=f"Name##{idx}", str=self.name)
            # TODO(orkaboy): Multiline?
            _, self.desc = imgui.input_text(label=f"Description##{idx}", str=self.desc)
            LayoutHelper.add_spacer()
            imgui.text("Primary Attributes")
            # Attributes
            _, self.cunning = imgui.slider_int(
                label=f"Cunning##{idx}", v=self.cunning, v_min=1, v_max=Faction.MAX_ATTRIBUTE
            )
            _, self.force = imgui.slider_int(
                label=f"Force##{idx}", v=self.force, v_min=1, v_max=Faction.MAX_ATTRIBUTE
            )
            _, self.wealth = imgui.slider_int(
                label=f"Wealth##{idx}", v=self.wealth, v_min=1, v_max=Faction.MAX_ATTRIBUTE
            )
            # TODO(orkaboy): real value
            _, self.magic = imgui.combo(
                label=f"Magic##{idx}", current_item=0, items=[x.name for x in MagicLevel]
            )
            LayoutHelper.add_spacer()
            # Secondary attributes
            imgui.text("Secondary Attributes")
            _, self.hp = imgui.input_int(label=f"HP##{idx}", v=self.hp)
            imgui.same_line()
            imgui.text(f"/{self.max_hp()}")
            _, self.treasure = imgui.input_int(label=f"Treasure##{idx}", v=self.treasure)
            LayoutHelper.add_spacer()
            # TODO(orkaboy): Render Tags
            imgui.text("Tags")
            for tag_idx, tag in enumerate(self.tags):
                tag.render(f"{idx}_{tag_idx}")
            LayoutHelper.add_spacer()
            imgui.text("Assets")
            # Render Assets
            for asset_type in [AssetType.CUNNING, AssetType.FORCE, AssetType.WEALTH]:
                assets_open, assets_visible = imgui.collapsing_header(
                    f"{asset_type.name}##{idx}", True, flags=32
                )
                if assets_open and assets_visible:
                    for asset_idx, asset in enumerate(self.assets_by_type(asset_type)):
                        asset.render(f"{idx}_{asset_idx}")
            LayoutHelper.add_spacer()
