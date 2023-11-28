from typing import Self

from imgui_bundle import imgui

from src.app import App
from src.faction import Faction, MagicLevel


class WwnApp(App):
    """Worlds Without Number specific App/GUI code."""

    def __init__(self: Self, config_data: dict) -> None:
        """Initialize WwnApp object."""
        super().__init__(config_data, title="Worlds Without Number - Faction Turn")

        self.factions: list[Faction] = [
            Faction("id1", "Dragon Empire", cunning=4, force=8, wealth=6, magic=MagicLevel.MEDIUM),
            Faction("id2", "Tali's Empire", cunning=6, force=5, wealth=5, magic=MagicLevel.MEDIUM),
            Faction("id3", "Shadow Council", cunning=8, force=8, wealth=6, magic=MagicLevel.HIGH),
        ]

    def execute(self: Self) -> None:
        """Draw GUI windows."""
        imgui.begin("Factions")

        imgui.set_window_pos("Factions", imgui.ImVec2(5, 5), imgui.Cond_.first_use_ever)
        imgui.set_window_size(imgui.ImVec2(240, 410), cond=imgui.Cond_.first_use_ever)

        for idx, faction in enumerate(self.factions):
            faction.render(idx)

        imgui.end()
