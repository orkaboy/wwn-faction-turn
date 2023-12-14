from copy import copy
from random import randint
from typing import Self
from uuid import uuid4

from imgui_bundle import imgui

from src.asset import Asset
from src.base_of_influence import BaseOfInfluence
from src.goal import Goal
from src.layout_helper import LayoutHelper
from src.location import Location
from src.style import STYLE
from src.system import AssetType, MagicLevel, goals_list
from src.tag import Tag


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
        self: Self,
        uuid: str,
        name: str,
        cunning: int = 1,
        force: int = 1,
        wealth: int = 1,
        magic: MagicLevel = MagicLevel.NONE,
    ) -> None:
        """Initialize Faction object."""
        self.name = name
        self.desc: str = ""
        self.uuid: str = uuid
        # Main faction attributes
        self.cunning: int = cunning
        self.force: int = force
        self.wealth: int = wealth
        self.magic: MagicLevel = magic
        # Secondary faction attributes
        self.exp: int = 0
        self.treasure: int = 0
        self.hp: int = self.max_hp()
        self.initiative: int = 0
        self.goal: Goal = None
        self.notes: str = ""
        # Asset tracking
        self.assets: list[Asset] = []
        self.bases: list[BaseOfInfluence] = []
        # Tags tracking
        self.tags: list[Tag] = []
        # Temporary variables
        self.goal_change_paralysis = False

    def __repr__(self: Self) -> str:
        return self.name

    def max_hp(self: Self) -> int:
        """Calculate faction max hp."""
        hp = 0
        hp += Faction.ATTRIBUTE_COST[self.cunning]
        hp += Faction.ATTRIBUTE_COST[self.force]
        hp += Faction.ATTRIBUTE_COST[self.wealth]
        return hp

    def roll_initiative(self: Self) -> None:
        """At the start of every faction turn, each faction rolls 1d8 for initiative, the highest rolls going first."""  # noqa: E501
        self.initiative = randint(1, 8)

    def get_attribute(self: Self, attribute: AssetType) -> int:
        """Return the value of an attribute, based on an AssetType."""
        match attribute:
            case AssetType.CUNNING:
                return self.cunning
            case AssetType.FORCE:
                return self.force
            case AssetType.WEALTH:
                return self.wealth
            case _:
                return 0

    def roll_attribute(self: Self, attribute: AssetType) -> int:
        """Make a roll on an attribute, based on an AssetType."""
        match attribute:
            case AssetType.CUNNING:
                return self.roll_cunning()
            case AssetType.FORCE:
                return self.roll_force()
            case AssetType.WEALTH:
                return self.roll_wealth()
            case _:
                return 0

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

    @staticmethod
    def _is_asset_type(asset: Asset, asset_type: AssetType) -> bool:
        if isinstance(asset.prototype, AssetType):
            return asset.prototype == asset_type
        return asset.prototype.type == asset_type

    def assets_by_type(self: Self, asset_type: AssetType) -> list[Asset]:
        """Return a list of all asset of a certain type."""
        return [asset for asset in self.assets if Faction._is_asset_type(asset, asset_type)]

    def asset_upkeep(self: Self) -> int:
        """The faction must pay any upkeep required by their individual Asset costs."""  # noqa: D401
        upkeep = 0
        # Sum up cost of assets
        for asset in self.assets:
            upkeep += asset.prototype.upkeep()
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

    def render(self: Self, idx: int, locations: list[Location]) -> None:
        """Render faction in GUI."""
        _, self.name = imgui.input_text(label=f"Name##{idx}", str=self.name)
        _, self.desc = imgui.input_text_multiline(label=f"Description##{idx}", str=self.desc)
        LayoutHelper.add_spacer()
        imgui.text("PRIMARY ATTRIBUTES")
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
        _, magic_value = imgui.combo(
            label=f"Magic##{idx}",
            current_item=self.magic.value,
            items=[x.name for x in MagicLevel],
        )
        self.magic = MagicLevel(magic_value)
        LayoutHelper.add_spacer()
        # Secondary attributes
        imgui.text("SECONDARY ATTRIBUTES")
        _, self.hp = imgui.input_int(
            label=f"HP##{idx}", v=self.hp, flags=imgui.InputTextFlags_.chars_decimal
        )
        imgui.same_line()
        imgui.text(f"/ {self.max_hp()}")
        _, self.treasure = imgui.input_int(
            label=f"Treasure##{idx}", v=self.treasure, flags=imgui.InputTextFlags_.chars_decimal
        )
        _, self.exp = imgui.input_int(
            label=f"Exp##{idx}", v=self.exp, flags=imgui.InputTextFlags_.chars_decimal
        )
        _, self.notes = imgui.input_text_multiline(
            label=f"Faction Notes##Faction_{self.uuid}", str=self.notes
        )
        LayoutHelper.add_spacer()
        # Render Tags
        tags_open = imgui.collapsing_header(
            f"TAGS ({len(self.tags)})##{idx}",
            flags=imgui.TreeNodeFlags_.default_open,
        )
        if tags_open:
            rm_tag = -1
            # Add new tag
            if imgui.button(f"Add Tag##{idx}"):
                self.tags.append(Tag(prototype=None))
            # Iterate over all faction tags
            for tag_idx, tag in enumerate(self.tags):
                tag.render(f"{idx}_{tag_idx}")
                # Remove button
                STYLE.button_color(STYLE.COL_RED)
                if imgui.button(f"X##rm_tag_{idx}_{tag_idx}"):
                    rm_tag = tag_idx
                STYLE.pop_color()
            # Remove any tag previously marked for removal
            if rm_tag != -1:
                self.tags.pop(rm_tag)

        LayoutHelper.add_spacer()
        # Goals
        imgui.text("CURRENT GOAL:")
        if self.goal:
            self.goal.render(f"Fact_{self.uuid}")
            STYLE.button_color(STYLE.COL_RED)
            if imgui.button(f"Clear goal##{idx}"):
                self.goal = None
            STYLE.pop_color()
        elif imgui.begin_combo(label="Set Goal##Turn", preview_value="Set faction goal"):
            for goal in goals_list():
                _, selected = imgui.selectable(
                    label=f"{goal.name}##Fact_{self.uuid}",
                    p_selected=False,
                )
                LayoutHelper.add_tooltip(goal.desc)
                if selected:
                    self.goal = copy(goal)
            imgui.end_combo()

        LayoutHelper.add_spacer()

        imgui.text("BASES OF INFLUENCE")
        if imgui.button(f"Add Base##{idx}"):
            self.bases.append(
                BaseOfInfluence(uuid=uuid4().hex, owner=self.uuid, location=None, max_hp=0)
            )
        rm_boi = -1
        for boi_idx, base in enumerate(self.bases):
            boi_open, boi_retain = imgui.collapsing_header(
                f"  {base.location}##{base.uuid}",
                True,
                flags=imgui.TreeNodeFlags_.default_open,
            )
            if boi_open and boi_retain:
                # Location
                if imgui.begin_combo(
                    label=f"Location##{base.uuid}", preview_value="Set base Location"
                ):
                    for loc in locations:
                        _, selected = imgui.selectable(
                            label=f"{loc}##{loc.uuid}",
                            p_selected=False,
                        )
                        LayoutHelper.add_tooltip(loc.desc)
                        if selected:
                            if base.location:
                                base.location.bases.remove(base)
                            base.location = loc
                            loc.bases.append(base)
                    imgui.end_combo()

                _, base.hp = imgui.input_int(label=f"HP##{base.uuid}", v=base.hp)
                _, base.max_hp = imgui.input_int(label=f"Max HP##{base.uuid}", v=base.max_hp)
                _, base.desc = imgui.input_text_multiline(
                    label=f"Description##{base.uuid}",
                    str=base.desc,
                )
            elif not boi_retain:
                rm_boi = boi_idx
        if rm_boi != -1:
            self.bases.pop(rm_boi)
        LayoutHelper.add_spacer()

        imgui.text("ASSETS")
        # Render Assets
        rm_asset = ""
        for type_idx, asset_type in enumerate(
            [AssetType.CUNNING, AssetType.FORCE, AssetType.WEALTH]
        ):
            assets = self.assets_by_type(asset_type)
            group_open = imgui.collapsing_header(
                f"{asset_type.name} ({len(assets)})##{idx}_{type_idx}",
                flags=imgui.TreeNodeFlags_.default_open,
            )
            if group_open:
                if imgui.button(f"Add Asset##{idx}_{type_idx}"):
                    self.assets.append(
                        Asset(prototype=asset_type, owner=self.uuid, uuid=uuid4().hex)
                    )
                # Iterate over all assets, by type
                for asset_idx, asset in enumerate(assets):
                    asset_open, asset_retain = imgui.collapsing_header(
                        f"  {asset}##{idx}_{type_idx}_{asset_idx}",
                        True,
                        flags=imgui.TreeNodeFlags_.default_open,
                    )
                    if asset_open and asset_retain:
                        asset.render(f"{idx}_{type_idx}_{asset_idx}", locations)
                    elif not asset_retain:
                        rm_asset = asset.uuid
            if type_idx < 3 - 1:
                LayoutHelper.add_spacer()
        # Remove asset if we've pressed the remove button
        if rm_asset != "":
            self.assets = [asset for asset in self.assets if asset.uuid != rm_asset]
