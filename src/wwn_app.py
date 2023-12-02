import logging
from enum import Enum, auto
from typing import Self
from uuid import uuid4

from imgui_bundle import imgui

from config import open_yaml, write_yaml
from src.app import App
from src.asset import AssetType
from src.faction import Faction
from src.layout_helper import LayoutHelper
from src.location import Location
from src.style import STYLE

logger = logging.getLogger(__name__)


DEFAULT_PROJECT = "Project/wwn.yaml"


class WwnApp(App):
    """Worlds Without Number specific App/GUI code."""

    class TurnFSM(Enum):
        IDLE = auto()
        # Go to next faction
        NEXT_FACTION = auto()
        # Main turn
        GAIN_TREASURE = auto()
        PAY_UPKEEP = auto()
        SPECIAL_ABILITIES = auto()
        MAIN_ACTION = auto()
        # <Actions>
        ACTION_ATTACK = auto()
        ACTION_MOVE_ASSET = auto()
        ACTION_REPAIR_ASSET = auto()
        ACTION_EXPAND_INFLUENCE = auto()
        ACTION_CREATE_ASSET = auto()
        ACTION_HIDE_ASSET = auto()
        ACTION_SELL_ASSET = auto()
        # </Actions>
        CHECK_GOAL = auto()

    def __init__(self: Self, config_data: dict) -> None:
        """Initialize WwnApp object."""
        super().__init__(config_data, title="Worlds Without Number - Faction Turn")
        self.factions: list[Faction] = []
        self.locations: list[Location] = []
        # Turn
        self.turn_order: list[Faction] = None
        self.cur_faction: int = 0
        self.state: WwnApp.TurnFSM = WwnApp.TurnFSM.IDLE
        # Load project data from file
        config_project: dict = config_data.get("project", {})
        self.project_filename: str = config_project.get("filename", DEFAULT_PROJECT)
        self.open_project()

    def _turn_active(self: Self) -> bool:
        # TODO(orkaboy): Currently doesn't allow save/load turning a turn
        return self.turn_order is not None

    def execute(self: Self) -> None:
        """Draw GUI windows."""
        self.faction_window()
        self.location_window()
        self.turn_window()

    def open_project(self: Self) -> None:
        """Load project from file."""
        project_data = open_yaml(self.project_filename)
        # TODO(orkaboy): Handle empty file and missing data
        # TODO(orkaboy): Parse from data
        self.factions = project_data.get("factions", [])
        self.locations = project_data.get("locations", [])

    def save_project(self: Self) -> None:
        """Save project to file."""
        # TODO(orkaboy): Fill in correct data
        data = {
            "factions": self.factions,
            "locations": self.locations,
        }
        write_yaml(filename=self.project_filename, data=data)

    def turn_logic(self: Self) -> None:
        """Execute turn logic according to the TurnFSM."""
        if self.cur_faction >= len(self.factions):
            self.turn_order = None
            self.state = WwnApp.TurnFSM.IDLE
            return
        faction = self.factions[self.cur_faction]
        # TODO(orkaboy): Logging
        match self.state:
            case WwnApp.TurnFSM.IDLE:
                self.cur_faction = 0
                imgui.text_wrapped(
                    "At the start of every faction turn, each faction rolls 1d8 for initiative, the highest rolls going first. Ties are resolved as the GM wishes, and then each faction takes the steps in order."  # noqa: E501
                )
                if imgui.button("Start first faction turn"):
                    self.state = WwnApp.TurnFSM.GAIN_TREASURE
            # Go to the next faction or end
            case WwnApp.TurnFSM.NEXT_FACTION:
                self.cur_faction += 1
                self.state = WwnApp.TurnFSM.GAIN_TREASURE
            # Main state machine
            case WwnApp.TurnFSM.GAIN_TREASURE:
                imgui.text_wrapped(
                    "1. The faction earns Treasure equal to half their Wealth plus a quarter of their combined Force and Cunning, the total being rounded up."  # noqa: E501
                )
                treasure_gain = faction.treasure_gain()
                imgui.text_wrapped(f"{faction.name} will gain {treasure_gain} Treasure.")
                if imgui.button("Apply treasure gain"):
                    faction.treasure += treasure_gain
                    self.state = WwnApp.TurnFSM.PAY_UPKEEP
            case WwnApp.TurnFSM.PAY_UPKEEP:
                imgui.text_wrapped(
                    "2. The faction must pay any upkeep required by their individual Asset costs, or by the cost of having too many Assets for their attributes. If they can't afford this upkeep, individual Assets may have their own bad consequences, while not being able to afford excess Assets means that the excess are lost."  # noqa: E501
                )
                asset_upkeep = faction.asset_upkeep()
                asset_total_excess = 0
                for asset_type in [AssetType.CUNNING, AssetType.FORCE, AssetType.WEALTH]:
                    assets = faction.assets_by_type(asset_type)
                    asset_excess = faction.asset_excess(asset_type)
                    imgui.text(
                        f"{asset_type.name} ASSETS ({len(assets)}/{faction.get_attribute(asset_type)}, excess cost: {asset_excess}):"  # noqa: E501
                    )
                    asset_total_excess += asset_excess
                    for asset in assets:
                        if (
                            asset.is_initialized()
                        ):  # Avoid crashing if asset.prototype isn't defined
                            imgui.text(f"{asset.name} (upkeep: {asset.prototype.upkeep()})")
                LayoutHelper.add_spacer()
                total_upkeep = asset_upkeep + asset_total_excess
                imgui.text(
                    f"Total upkeep for {faction.name} to pay is {asset_upkeep} + {asset_excess} = {total_upkeep}. Remove excess assets if unable to pay."  # noqa: E501
                )
                if imgui.button("Pay upkeep"):
                    faction.treasure = max(0, faction.treasure - total_upkeep)
                    self.state = WwnApp.TurnFSM.SPECIAL_ABILITIES
            case WwnApp.TurnFSM.SPECIAL_ABILITIES:
                imgui.text_wrapped(
                    "3. The faction triggers any special abilities individual Assets may have, such as abilities that allow an Asset to move or perform some other special benefit."  # noqa: E501
                )
            # TODO(orkaboy): continue

    def turn_window(self: Self) -> None:
        """Draw turn logic GUI."""
        imgui.begin("Turn")

        imgui.set_window_pos("Turn", imgui.ImVec2(245, 5), imgui.Cond_.first_use_ever)
        imgui.set_window_size(imgui.ImVec2(240, 410), cond=imgui.Cond_.first_use_ever)

        if self._turn_active():
            # Print out the turn order and progress
            imgui.text("TURN ORDER:")
            for idx, faction in enumerate(self.turn_order):
                if idx == self.cur_faction:
                    imgui.text(f"{faction.initiative}: {faction.name} (CURRENT)")
                else:
                    imgui.text(f"{faction.initiative}: {faction.name}")

            # Execute main turn logic
            LayoutHelper.add_spacer()
            self.turn_logic()
            LayoutHelper.add_spacer()

            # End turn, next faction etc.
            STYLE.button_color(STYLE.COL_RED)
            if imgui.button("Skip faction"):
                self.state = WwnApp.TurnFSM.NEXT_FACTION
            if imgui.button("Abort Turn"):
                # TODO(orkaboy): Currently doesn't rollback changes made
                self.turn_order = None
                self.state = WwnApp.TurnFSM.IDLE
            STYLE.pop_color()
        else:
            if imgui.button("New Turn"):
                for faction in self.factions:
                    faction.roll_initiative()
                self.turn_order = sorted(
                    self.factions.copy(), key=lambda faction: faction.initiative, reverse=True
                )
                self.state = WwnApp.TurnFSM.IDLE
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
