import logging
from copy import copy
from enum import Enum, auto
from math import ceil, floor
from typing import Self
from uuid import uuid4

from imgui_bundle import imgui

from config import open_yaml, write_yaml
from src.app import App
from src.asset import Asset, AssetType
from src.base_of_influence import BaseOfInfluence
from src.faction import Faction
from src.layout_helper import LayoutHelper
from src.location import Location
from src.style import STYLE
from src.system import QUALITY, goals_list

logger = logging.getLogger(__name__)


DEFAULT_PROJECT = "Project/wwn.yaml"


class WwnApp(App):
    """Worlds Without Number specific App/GUI code."""

    HIDE_ACTION_CUNNING_REQUIREMENT = 3
    HIDE_ACTION_COST = 2

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
        self.turn: int = 0
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
        self.turn = project_data.get("turn", 0)

    def save_project(self: Self) -> None:
        """Save project to file."""
        # TODO(orkaboy): Fill in correct data
        data = {
            "factions": self.factions,
            "locations": self.locations,
            "turn": self.turn,
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
                            imgui.text(
                                f"{asset} (upkeep: {asset.prototype.upkeep()}), location: {asset.loc}"  # noqa: E501
                            )
                            LayoutHelper.add_tooltip(
                                f"{asset.desc}\n\n{asset.prototype.strings.rules}"
                            )
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
                for asset in faction.assets:
                    if asset.is_initialized():  # Avoid crashing if asset.prototype isn't defined
                        imgui.text(f"{asset}, location: {asset.loc}")
                        LayoutHelper.add_tooltip(f"{asset.desc}\n\n{asset.prototype.strings.rules}")
                        if QUALITY.Action in asset.qualities:
                            imgui.same_line()
                            imgui.text("ACTION")
                        if QUALITY.Special in asset.qualities:
                            imgui.same_line()
                            imgui.text("SPECIAL")
                LayoutHelper.add_spacer()
                if imgui.button("Done with special actions"):
                    self.state = WwnApp.TurnFSM.MAIN_ACTION
            case WwnApp.TurnFSM.MAIN_ACTION:
                imgui.text_wrapped(
                    "4. The faction takes one Faction Action as listed below, resolving any Attacks or other consequences from their choice. When an action is taken, every Asset owned by the faction may take it; thus, if Attack is chosen, then every valid Asset owned by the faction can Attack. If Repair Asset is chosen, every Asset can be repaired if enough Treasure is spent."  # noqa: E501
                )

                no_assets = len(faction.assets) == 0

                # Only allow Attack, Move Asset, Repair Asset if the faction has assets
                if no_assets:
                    imgui.begin_disabled()

                if imgui.button("Attack"):
                    self.state = WwnApp.TurnFSM.ACTION_ATTACK
                if no_assets:
                    LayoutHelper.add_tooltip("No assets to attack with.")

                if imgui.button("Move Asset"):
                    self.state = WwnApp.TurnFSM.ACTION_MOVE_ASSET
                if no_assets:
                    LayoutHelper.add_tooltip("No assets to move.")

                if imgui.button("Repair Asset"):
                    self.state = WwnApp.TurnFSM.ACTION_REPAIR_ASSET

                if no_assets:
                    LayoutHelper.add_tooltip("No assets to repair.")
                    imgui.end_disabled()

                if imgui.button("Expand Influence"):
                    self.state = WwnApp.TurnFSM.ACTION_EXPAND_INFLUENCE
                if imgui.button("Create Asset"):
                    self.state = WwnApp.TurnFSM.ACTION_CREATE_ASSET
                # Hide is an action available only to factions with a Cunning score of 3 or better
                can_hide = faction.cunning >= WwnApp.HIDE_ACTION_CUNNING_REQUIREMENT
                if not can_hide:
                    imgui.begin_disabled()
                if imgui.button("Hide Asset"):
                    self.state = WwnApp.TurnFSM.ACTION_HIDE_ASSET
                if not can_hide:
                    LayoutHelper.add_tooltip("Faction must have a Cunning score of 3 or higher.")
                    imgui.end_disabled()

                # Only allow Sell Asset if the faction has assets
                if no_assets:
                    imgui.begin_disabled()
                if imgui.button("Sell Asset"):
                    self.state = WwnApp.TurnFSM.ACTION_SELL_ASSET
                if no_assets:
                    LayoutHelper.add_tooltip("No assets to sell.")
                    imgui.end_disabled()

                if imgui.button("Skip Main Action"):
                    self.state = WwnApp.TurnFSM.CHECK_GOAL
                LayoutHelper.add_tooltip("Skip the faction's main action this turn.")

            case (
                WwnApp.TurnFSM.ACTION_ATTACK
                | WwnApp.TurnFSM.ACTION_MOVE_ASSET
                | WwnApp.TurnFSM.ACTION_REPAIR_ASSET
                | WwnApp.TurnFSM.ACTION_EXPAND_INFLUENCE
                | WwnApp.TurnFSM.ACTION_CREATE_ASSET
                | WwnApp.TurnFSM.ACTION_HIDE_ASSET
                | WwnApp.TurnFSM.ACTION_SELL_ASSET
            ):
                self.main_action()

                LayoutHelper.add_spacer()

                if imgui.button(label="Back##Action"):
                    self.state = WwnApp.TurnFSM.MAIN_ACTION
                if imgui.button(label="Done##Action"):
                    self.state = WwnApp.TurnFSM.CHECK_GOAL

            case WwnApp.TurnFSM.CHECK_GOAL:
                imgui.text_wrapped(
                    "The faction checks to see if it's accomplished its most recent goal. If so, it collects the experience points for doing so and picks a new goal. If not, it can abandon the old goal and pick a new one, but it will sacrifice its next turn's Faction Action to do so and may not trigger any Asset special abilities that round, either."  # noqa: E501
                )
                LayoutHelper.add_spacer()

                # Goals
                imgui.text("CURRENT GOAL:")
                if faction.goal:
                    faction.goal.render(f"Turn_{faction.uuid}")
                    if imgui.button("Complete goal"):
                        faction.exp += faction.goal.difficulty
                        faction.goal = None
                elif imgui.begin_combo(label="Set Goal##Turn", preview_value="Set faction goal"):
                    for goal in goals_list():
                        _, selected = imgui.selectable(
                            label=f"{goal.name}##Turn_{faction.uuid}",
                            p_selected=False,
                        )
                        LayoutHelper.add_tooltip(goal.desc)
                        if selected:
                            faction.goal = copy(goal)
                    imgui.end_combo()
                STYLE.button_color(STYLE.COL_RED)
                if faction.goal and imgui.button("Abort goal"):
                    # TODO(orkaboy): Mark as paralyzed next turn
                    faction.goal = None
                STYLE.pop_color()

                LayoutHelper.add_spacer()
                # TODO(orkaboy): Upgrade stats for exp
                LayoutHelper.add_spacer()

                if imgui.button("COMPLETE TURN##Turn"):
                    self.state = WwnApp.TurnFSM.NEXT_FACTION

    def main_action(self: Self) -> None:
        """Display main action part of statemachine."""
        faction = self.factions[self.cur_faction]

        # TODO(orkaboy): continue
        match self.state:
            case WwnApp.TurnFSM.ACTION_ATTACK:
                imgui.text("ATTACK:")
                imgui.text_wrapped(
                    """The faction nominates one or more Assets to attack the enemy in their locations. In each location, the defender chooses which of the Assets present will meet the Attack; thus, if a unit of Infantry attacks in a location where there is an enemy Base of Influence, Informers, and Idealistic Thugs, the defender could decide to use Idealistic Thugs to defend against the attack.
The attacker makes an attribute check based on the attack of the acting Asset; thus, the Infantry would roll Force versus Force. On a success, the defending Asset takes damage equal to the attacking Asset's attack score, or 1d8 in the case of Infantry. On a failure, the attacking Asset takes damage equal to the defending Asset's counterattack score, or 1d6 in the case of Idealistic Thugs.
If the damage done to an Asset reduces it to zero hit points, it is destroyed. The same Asset may be used to defend against multiple attacking Assets, provided it can survive the onslaught.
Damage done to a Base of Influence is also done directly to the faction's hit points. Overflow damage is not transmitted, however; if the Base of Influence only has 5 hit points and 7 hit points are inflicted, the faction loses the Base of Influence and 5 hit points from its total."""  # noqa: E501
                )

                # TODO(orkaboy): continue
            case WwnApp.TurnFSM.ACTION_MOVE_ASSET:
                imgui.text("MOVE ASSET:")
                imgui.text_wrapped(
                    """One or more Assets are moved up to one turn's worth of movement each. The receiving location must not have the ability and inclination to forbid the Asset from operating there. Subtle and Stealthed Assets ignore this limit.
If an asset loses the Subtle or Stealth qualities while in a hostile location, they must use this action to retreat to safety within one turn or they will take half their maximum hit points in damage at the start of the next turn, rounded up."""  # noqa: E501
                )

                # TODO(orkaboy): continue
            case WwnApp.TurnFSM.ACTION_REPAIR_ASSET:
                imgui.text("REPAIR ASSET:")
                imgui.text_wrapped(
                    """The faction spends 1 Treasure on each Asset they wish to repair, fixing half their relevant attribute value in lost hit points, rounded up. Thus, fixing a Force Asset would heal half the faction's Force attribute, rounded up. Additional healing can be applied to an Asset in this same turn, but the cost increases by 1 Treasure for each subsequent fix; thus, the second costs 2 Treasure, the third costs 3 Treasure, and so forth.
This ability can at the same time also be used to repair damage done to the faction, spending 1 Treasure to heal a total equal to the faction's highest and lowest Force, Wealth, or Cunning attribute divided by two, rounded up. Thus, a faction with a Force of 5, Wealth of 2, and Cunning of 4 would heal 4 points of damage. Only one such application of healing is possible for a faction each turn."""  # noqa: E501
                )

                for asset in faction.assets:
                    if not asset.is_initialized():
                        continue

                    full_hp: bool = asset.hp == asset.max_hp()
                    if not full_hp:
                        asset.render_brief()
                        imgui.same_line()
                        attribute = faction.get_attribute(asset.prototype.type)
                        repair_amount = ceil(attribute / 2)
                        # TODO(orkaboy): Multiple repairs cost more during same turn!
                        repair_cost = 1
                        disabled = faction.treasure < repair_cost
                        if disabled:
                            imgui.begin_disabled()
                        if imgui.button(label=f"Repair##{asset.uuid}"):
                            faction.treasure -= repair_cost
                            asset.hp = min(asset.max_hp(), asset.hp + repair_amount)
                        LayoutHelper.add_tooltip(
                            f"Repair up to {repair_amount} HP on Asset for {repair_cost} Treasure"
                        )
                        if disabled:
                            imgui.end_disabled()

                # Repair faction button
                high_attr = max(faction.cunning, faction.force, faction.wealth)
                low_attr = min(faction.cunning, faction.force, faction.wealth)
                repair_amount = ceil((high_attr + low_attr) / 2)
                repair_cost = 1
                # TODO(orkaboy): Only available once per turn
                disabled = faction.treasure < repair_cost
                if disabled:
                    imgui.begin_disabled()
                if imgui.button("Repair faction"):
                    faction.treasure -= repair_cost
                    faction.hp = min(faction.max_hp(), faction.hp + repair_amount)
                LayoutHelper.add_tooltip(
                    f"Repair faction for up to {repair_amount} HP, for {repair_cost} Treasure"
                )
                if disabled:
                    imgui.end_disabled()

            case WwnApp.TurnFSM.ACTION_EXPAND_INFLUENCE:
                imgui.text("EXPAND INFLUENCE:")
                imgui.text_wrapped(
                    """The faction seeks to establish a new base of operations in a location. The faction must have at least one Asset there already to make this attempt, and must spend 1 Treasure for each hit point the new Base of Influence is to have. Thus, to create a new Base of Influence with a maximum hit point total of 10, 10 Treasure must be spent. Bases with high maximum hit point totals are harder to dislodge, but losing them also inflicts much more damage on the faction's own hit points.
Once the Base of Influence is created, the owner makes a Cunning versus Cunning attribute check against every other faction that has at least one Asset in the same location. If the other faction wins the check, they are allowed to make an immediate Attack against the new Base of Influence with whatever Assets they have present in the location. The creating faction may attempt to block this action by defending with other Assets present.
If the Base of Influence survives this onslaught, it operates as normal and allows the faction to purchase new Assets there with the Create Asset action."""  # noqa: E501
                )
                # TODO(orkaboy): continue
            case WwnApp.TurnFSM.ACTION_CREATE_ASSET:
                imgui.text("CREATE ASSET:")
                imgui.text_wrapped(
                    """The faction buys one Asset at a location where they have a Base of Influence. They must have the minimum attribute and Magic ratings necessary to buy the Asset and must pay the listed cost in Treasure to build it. A faction can create only one Asset per turn.
A faction can have no more Assets of a particular attribute than their attribute score. Thus, a faction with a Force of 3 can have only 3 Force Assets. If this number is exceeded, the faction must pay 1 Treasure per excess Asset at the start of each turn, or else they will lose the excess."""  # noqa: E501
                )
                # TODO(orkaboy): continue
            case WwnApp.TurnFSM.ACTION_HIDE_ASSET:
                imgui.text("HIDE ASSET:")
                imgui.text_wrapped(
                    "An action available only to factions with a Cunning score of 3 or better, this action allows the faction to give one owned Asset the Stealth quality for every 2 Treasure they spend. Assets currently in a location with another faction's Base of Influence can't be hidden. If the Asset later loses the Stealth, no refund is given."  # noqa: E501
                )

                for asset in faction.assets:
                    if not asset.is_initialized():
                        continue

                    if QUALITY.Stealth not in asset.qualities:
                        asset.render_brief()
                        imgui.same_line()
                        # TODO(orkaboy): Disable if rival faction has Base of Influence in location
                        disabled = faction.treasure < WwnApp.HIDE_ACTION_COST
                        if disabled:
                            imgui.begin_disabled()
                        if imgui.button(label=f"Add Stealth for 2 Treasure##{asset.uuid}"):
                            faction.treasure -= WwnApp.HIDE_ACTION_COST
                            asset.qualities.append(QUALITY.Stealth)
                        if disabled:
                            LayoutHelper.add_tooltip("Cannot afford to add Stealth to asset.")
                            imgui.end_disabled()
            case WwnApp.TurnFSM.ACTION_SELL_ASSET:
                imgui.text("SELL ASSET:")
                imgui.text_wrapped(
                    "The faction voluntarily decommissions an Asset, salvaging it for what it's worth. The Asset is lost and the faction gains half its purchase cost in Treasure, rounded down. If the Asset is damaged when it is sold, however, no Treasure is gained."  # noqa: E501
                )

                rm_asset = -1
                for idx, asset in enumerate(faction.assets):
                    if not asset.is_initialized():
                        continue

                    asset.render_brief()
                    full_hp: bool = asset.hp == asset.max_hp()
                    sell_price: int = floor(asset.prototype.requirements.cost / 2) if full_hp else 0
                    imgui.same_line()
                    if imgui.button(f"Sell Asset for {sell_price} Treasure##{asset.uuid}"):
                        faction.treasure += sell_price
                        rm_asset = idx
                if rm_asset != -1:
                    faction.assets.pop(rm_asset)
            case _:
                imgui.text("ERROR STATE")

    def turn_window(self: Self) -> None:
        """Draw turn logic GUI."""
        imgui.begin("Turn")

        imgui.set_window_pos("Turn", imgui.ImVec2(245, 5), imgui.Cond_.first_use_ever)
        imgui.set_window_size(imgui.ImVec2(240, 410), cond=imgui.Cond_.first_use_ever)

        imgui.text(f"Turn {self.turn}")
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
            _, faction.notes = imgui.input_text_multiline(
                label=f"Faction Notes##Turn_{faction.uuid}", str=faction.notes
            )

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
                self.turn += 1
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
