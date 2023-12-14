import logging
from typing import Self
from uuid import uuid4

from imgui_bundle import imgui

from config import open_yaml, write_yaml
from src.app import App
from src.asset import Asset
from src.base_of_influence import BaseOfInfluence
from src.faction import Faction
from src.layout_helper import LayoutHelper
from src.location import Location
from src.system import QUALITY
from src.turn import FactionTurn

logger = logging.getLogger(__name__)


DEFAULT_PROJECT = "Project/wwn.yaml"


class WwnApp(App):
    """Worlds Without Number specific App/GUI code."""

    def __init__(self: Self, config_data: dict) -> None:
        """Initialize WwnApp object."""
        super().__init__(config_data, title="Worlds Without Number - Faction Turn")
        self.factions: list[Faction] = []
        self.locations: list[Location] = []
        self.turn: FactionTurn = FactionTurn()
        # Load project data from file
        config_project: dict = config_data.get("project", {})
        self.project_filename: str = config_project.get("filename", DEFAULT_PROJECT)
        self.open_project()

    def execute(self: Self) -> None:
        """Draw GUI windows."""
        self.faction_window()
        self.location_window()
        self.turn.execute(self.factions)
        self.project_window()

    def open_project(self: Self) -> None:
        """Load project from file."""
        project_data = open_yaml(self.project_filename)
        # TODO(orkaboy): Handle empty file and missing data
        # TODO(orkaboy): Parse from data
        self.factions = project_data.get("factions", [])
        self.locations = project_data.get("locations", [])
        self.turn = project_data.get("turn", FactionTurn())

    def save_project(self: Self) -> None:
        """Save project to file."""
        # TODO(orkaboy): Fill in correct data
        data = {
            "factions": self.factions,
            "locations": self.locations,
            "turn": self.turn,
        }
        write_yaml(filename=self.project_filename, data=data)

    def project_window(self: Self) -> None:
        """Draw project GUI."""
        imgui.begin("Project")

        imgui.set_window_pos("Project", imgui.ImVec2(500, 5), imgui.Cond_.first_use_ever)
        imgui.set_window_size(imgui.ImVec2(240, 410), cond=imgui.Cond_.first_use_ever)

        # Save project to file
        _, self.project_filename = imgui.input_text(label="Filename", str=self.project_filename)
        if imgui.button("Save project"):
            self.save_project()
        imgui.same_line()
        if imgui.button("Load project"):
            self.open_project()

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
                _, loc.name = imgui.input_text(label=f"Name##Loc_{loc.uuid}", str=loc.name)
                _, loc.desc = imgui.input_text_multiline(
                    label=f"Description##Loc_{loc.uuid}", str=loc.desc
                )
                imgui.text("BASES:")
                for base_cast in loc.bases:
                    base: BaseOfInfluence = base_cast
                    base_owner: Faction = None
                    for faction in self.factions:
                        if faction.uuid == base.owner:
                            base_owner = faction
                            break
                    imgui.text(f"{base_owner} ({base.hp}/{base.max_hp})")
                    LayoutHelper.add_tooltip(text=base.desc)
                imgui.text("ASSETS:")
                for asset_cast in loc.assets:
                    asset: Asset = asset_cast
                    asset_owner: Faction = None
                    for faction in self.factions:
                        if faction.uuid == asset.owner:
                            asset_owner = faction
                            break
                    imgui.text(f"{asset_owner}: {asset} ({asset.hp}/{asset.max_hp()})")
                    if QUALITY.Stealth in asset.qualities:
                        imgui.same_line()
                        imgui.text("STEALTH")
                    if QUALITY.Subtle in asset.qualities:
                        imgui.same_line()
                        imgui.text("SUBTLE")
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
                faction.render(idx, self.locations)
            if not faction_retain:
                rm_faction = idx
            if idx < len(self.factions) - 1:
                LayoutHelper.add_spacer(2)
        if rm_faction >= 0:
            self.factions.pop(rm_faction)

        imgui.end()
