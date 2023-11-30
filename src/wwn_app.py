from typing import Self
from uuid import uuid4

from imgui_bundle import imgui

from src.app import App
from src.faction import Faction
from src.layout_helper import LayoutHelper
from src.style import STYLE


class WwnApp(App):
    """Worlds Without Number specific App/GUI code."""

    def __init__(self: Self, config_data: dict) -> None:
        """Initialize WwnApp object."""
        super().__init__(config_data, title="Worlds Without Number - Faction Turn")
        self.factions: list[Faction] = []
        self.turn_order: list[Faction] = None

    def _turn_active(self: Self) -> bool:
        return self.turn_order is not None

    def execute(self: Self) -> None:
        """Draw GUI windows."""
        self.faction_window()
        self.turn_window()

    def turn_window(self: Self) -> None:
        """Draw turn logic GUI."""
        imgui.begin("Turn")

        imgui.set_window_pos("Turn", imgui.ImVec2(245, 5), imgui.Cond_.first_use_ever)
        imgui.set_window_size(imgui.ImVec2(240, 410), cond=imgui.Cond_.first_use_ever)

        if self._turn_active():
            for faction in self.turn_order:
                imgui.text(f"{faction.initiative}: {faction.name}")
            # TODO(orkaboy): End turn, next faction etc.
            STYLE.button_color(STYLE.COL_RED)
            if imgui.button("Abort Turn"):
                self.turn_order = None
            STYLE.pop_color()
        elif imgui.button("New Turn"):
            for faction in self.factions:
                faction.roll_initiative()
            self.turn_order = sorted(
                self.factions.copy(), key=lambda faction: faction.initiative, reverse=True
            )

        imgui.end()

    def faction_window(self: Self) -> None:
        """Draw faction browser GUI."""
        imgui.begin("Factions")

        imgui.set_window_pos("Factions", imgui.ImVec2(5, 5), imgui.Cond_.first_use_ever)
        imgui.set_window_size(imgui.ImVec2(240, 410), cond=imgui.Cond_.first_use_ever)

        if imgui.button("Add Faction"):
            self.factions.append(
                Faction(ident=uuid4().hex, name="New Faction"),
            )

        rm_faction = -1
        for idx, faction in enumerate(self.factions):
            faction_open, faction_retain = imgui.collapsing_header(
                f"{faction.name}##{idx}", True, flags=imgui.TreeNodeFlags_.default_open
            )
            if faction_open and faction_retain:
                faction.render(idx)
            if not faction_retain:
                rm_faction = idx
            if idx < len(self.factions) - 1:
                LayoutHelper.add_spacer(2)
        if rm_faction >= 0:
            self.factions.pop(rm_faction)

        imgui.end()
