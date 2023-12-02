import logging
from typing import Self
from uuid import uuid4

from imgui_bundle import imgui

from config import open_yaml
from src.app import App
from src.faction import Faction
from src.layout_helper import LayoutHelper
from src.location import Location
from src.style import STYLE

logger = logging.getLogger(__name__)


DEFAULT_PROJECT = "Project/wwn.yaml"


class WwnApp(App):
    """Worlds Without Number specific App/GUI code."""

    def __init__(self: Self, config_data: dict) -> None:
        """Initialize WwnApp object."""
        super().__init__(config_data, title="Worlds Without Number - Faction Turn")
        self.factions: list[Faction] = []
        self.locations: list[Location] = []
        self.turn_order: list[Faction] = None
        # Load project data from file
        config_project: dict = config_data.get("project", {})
        config_filename: str = config_project.get("filename", DEFAULT_PROJECT)
        self.project_data = open_yaml(config_filename)

    def _turn_active(self: Self) -> bool:
        return self.turn_order is not None

    def execute(self: Self) -> None:
        """Draw GUI windows."""
        self.faction_window()
        self.location_window()
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

    def location_window(self: Self) -> None:
        """Draw location browser GUI."""
        imgui.begin("Locations")

        imgui.set_window_pos("Turn", imgui.ImVec2(500, 5), imgui.Cond_.first_use_ever)
        imgui.set_window_size(imgui.ImVec2(240, 410), cond=imgui.Cond_.first_use_ever)

        if imgui.button("Add Location"):
            self.locations.append(Location(uuid=uuid4().hex, name="New Location"))

        rm_loc = -1
        for idx, loc in enumerate(self.locations):
            loc_open, loc_retain = imgui.collapsing_header(
                label=f"{loc}##{loc.uuid}", p_visible=True, flags=imgui.TreeNodeFlags_.default_open
            )

            if loc_open and loc_retain:
                _, loc.name = imgui.input_text(label="Name", str=loc.name)
                _, loc.desc = imgui.input_text_multiline(label="Description", str=loc.desc)
                imgui.text("ASSETS:")
                for asset_id in loc.asset_ids:
                    asset = None
                    for faction in self.factions:
                        for f_asset in faction.assets:
                            if asset_id == f_asset.uuid:
                                asset = f_asset
                                break
                        if asset:
                            break
                    if asset:
                        imgui.text(asset.name())
                        LayoutHelper.add_tooltip(text=asset.desc)
            if not loc_retain:
                rm_loc = idx
        if rm_loc >= 0:
            self.locations.pop(rm_loc)

        imgui.end()

    def faction_window(self: Self) -> None:
        """Draw faction browser GUI."""
        imgui.begin("Factions")

        imgui.set_window_pos("Factions", imgui.ImVec2(5, 5), imgui.Cond_.first_use_ever)
        imgui.set_window_size(imgui.ImVec2(240, 410), cond=imgui.Cond_.first_use_ever)

        if imgui.button("Add Faction"):
            self.factions.append(
                Faction(uuid=uuid4().hex, name="New Faction"),
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
