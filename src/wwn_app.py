from typing import Self

from imgui_bundle import imgui

from src.app import App


class WwnApp(App):
    """Worlds Without Number specific App/GUI code."""

    def __init__(self: Self, config_data: dict) -> None:
        super().__init__(config_data, title="Worlds Without Number - Faction Turn")

    def execute(self: Self) -> None:
        """Draw GUI windows."""
        imgui.begin("Factions")

        imgui.set_window_pos("Factions", imgui.ImVec2(5, 5), imgui.Cond_.first_use_ever)
        imgui.set_window_size(imgui.ImVec2(240, 410), cond=imgui.Cond_.first_use_ever)

        imgui.end()
