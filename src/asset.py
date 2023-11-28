from copy import copy
from enum import Enum, auto
from typing import Self

from imgui_bundle import imgui


class AssetType(Enum):
    CUNNING = auto()
    FORCE = auto()
    WEALTH = auto()


class Asset:
    def __init__(
        self: Self,
        name: str,
        ident: str,
        asset_type: AssetType,
        damage_formula: str,
        rules: str,
        cost: int,
        max_hp: int,
        upkeep: int = 0,
    ) -> None:
        """Initialize Asset object."""
        self.name: str = name
        self.id: str = ident
        # Static descriptions
        self.type = asset_type
        self.rules: str = rules
        self.damage_formula: str = damage_formula
        # Stats (shared between all instances)
        self.cost: int = cost
        self.max_hp: int = max_hp
        self.upkeep: int = upkeep
        # Variable stats
        self.desc: str = ""
        self.owner: str = ""
        self.hp: int = self.max_hp

    def instantiate(self: Self, owner: str) -> Self:
        """Create a unique instance from the asset prototype."""
        asset_copy = copy(self)
        # Assign owner and hp
        asset_copy.owner = owner
        self.hp: int = self.max_hp
        return asset_copy

    def roll_damage(self: Self) -> int:
        """Need to override with asset damage formula."""
        return 0

    def render(self: Self, idx: str) -> None:
        """Render asset in GUI."""
        _, self.name = imgui.input_text(label="Name", str=self.name)
        # TODO(orkaboy): Multiline?
        _, self.desc = imgui.input_text(label="Description", str=self.desc)
        _, self.hp = imgui.input_int(label="HP", v=self.hp)
        _, self.hp = imgui.input_int(label="HP", v=self.hp)
        imgui.same_line()
        imgui.text(f"/{self.max_hp}")
        imgui.text_wrapped(self.damage_formula)
        imgui.text_wrapped(self.rules)
        if self.upkeep:
            imgui.text(f"Upkeep: {self.upkeep}")
        # TODO(orkaboy): RM button
        if imgui.button(f"Remove##{idx}"):
            pass
