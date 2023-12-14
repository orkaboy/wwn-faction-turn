import logging
from copy import copy
from enum import Enum, auto
from math import ceil, floor
from typing import Self
from uuid import uuid4

from imgui_bundle import imgui

from src.asset import Asset, AssetPrototype, AssetType
from src.base_of_influence import BaseOfInfluence
from src.faction import Faction
from src.layout_helper import LayoutHelper
from src.location import Location
from src.style import STYLE
from src.system import QUALITY, MagicLevel, cunning_list, force_list, goals_list, wealth_list

logger = logging.getLogger(__name__)


class FactionTurn:
    """Worlds Without Number turn logic code."""

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

    def __init__(self: Self) -> None:
        """Initialize FactionTurn object."""
        # Turn counter
        self.turn_idx: int = 0
        # Turn variables
        self.turn_order: list[Faction] = None
        self.cur_faction: int = 0
        self.state: FactionTurn.TurnFSM = FactionTurn.TurnFSM.IDLE
        # Temp choice variables
        self.asset_to_buy: AssetPrototype = None
        self.asset_to_buy_loc: Location = None
        self.boi_loc: Location = None
        self.boi_hp: int = 0
        self.repaired_faction: bool = False

    def _turn_active(self: Self) -> bool:
        return self.turn_order is not None

    def _new_turn(self: Self) -> None:
        """Clear temp variables and enter first FSM state."""
        self.state = FactionTurn.TurnFSM.GAIN_TREASURE
        self.repaired_faction = False
        self.asset_to_buy = None
        self.asset_to_buy_loc = None
        self.boi_loc = None
        self.boi_hp = 0

    def turn_logic(self: Self, factions: list[Faction]) -> None:
        """Execute turn logic according to the TurnFSM."""
        if self.cur_faction >= len(factions):
            self.turn_order = None
            self.state = FactionTurn.TurnFSM.IDLE
            self.cur_faction = 0
            return
        faction = factions[self.cur_faction]

        # TODO(orkaboy): Logging
        match self.state:
            case FactionTurn.TurnFSM.IDLE:
                self.cur_faction = 0
                imgui.text_wrapped(
                    "At the start of every faction turn, each faction rolls 1d8 for initiative, the highest rolls going first. Ties are resolved as the GM wishes, and then each faction takes the steps in order."  # noqa: E501
                )
                if imgui.button("Start first faction turn"):
                    self._new_turn()

            # Go to the next faction or end
            case FactionTurn.TurnFSM.NEXT_FACTION:
                self.cur_faction += 1
                self._new_turn()
            # Main state machine

            case FactionTurn.TurnFSM.GAIN_TREASURE:
                imgui.text_wrapped(
                    "1. The faction earns Treasure equal to half their Wealth plus a quarter of their combined Force and Cunning, the total being rounded up."  # noqa: E501
                )
                treasure_gain = faction.treasure_gain()
                imgui.text_wrapped(f"{faction.name} will gain {treasure_gain} Treasure.")
                if imgui.button("Apply treasure gain"):
                    faction.treasure += treasure_gain
                    self.state = FactionTurn.TurnFSM.PAY_UPKEEP

            case FactionTurn.TurnFSM.PAY_UPKEEP:
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
                    self.state = FactionTurn.TurnFSM.SPECIAL_ABILITIES

            case FactionTurn.TurnFSM.SPECIAL_ABILITIES:
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
                    self.state = FactionTurn.TurnFSM.MAIN_ACTION

            case FactionTurn.TurnFSM.MAIN_ACTION:
                imgui.text_wrapped(
                    "4. The faction takes one Faction Action as listed below, resolving any Attacks or other consequences from their choice. When an action is taken, every Asset owned by the faction may take it; thus, if Attack is chosen, then every valid Asset owned by the faction can Attack. If Repair Asset is chosen, every Asset can be repaired if enough Treasure is spent."  # noqa: E501
                )

                no_assets = len(faction.assets) == 0

                # Only allow Attack, Move Asset, Repair Asset if the faction has assets
                if no_assets:
                    imgui.begin_disabled()

                if imgui.button("Attack"):
                    self.state = FactionTurn.TurnFSM.ACTION_ATTACK
                if no_assets:
                    LayoutHelper.add_tooltip("No assets to attack with.")

                if imgui.button("Move Asset"):
                    self.state = FactionTurn.TurnFSM.ACTION_MOVE_ASSET
                if no_assets:
                    LayoutHelper.add_tooltip("No assets to move.")

                if imgui.button("Repair Asset"):
                    self.state = FactionTurn.TurnFSM.ACTION_REPAIR_ASSET

                if no_assets:
                    LayoutHelper.add_tooltip("No assets to repair.")
                    imgui.end_disabled()

                if imgui.button("Expand Influence"):
                    self.state = FactionTurn.TurnFSM.ACTION_EXPAND_INFLUENCE
                if imgui.button("Create Asset"):
                    self.state = FactionTurn.TurnFSM.ACTION_CREATE_ASSET
                # Hide is an action available only to factions with a Cunning score of 3 or better
                can_hide = faction.cunning >= FactionTurn.HIDE_ACTION_CUNNING_REQUIREMENT
                if not can_hide:
                    imgui.begin_disabled()
                if imgui.button("Hide Asset"):
                    self.state = FactionTurn.TurnFSM.ACTION_HIDE_ASSET
                if not can_hide:
                    LayoutHelper.add_tooltip("Faction must have a Cunning score of 3 or higher.")
                    imgui.end_disabled()

                # Only allow Sell Asset if the faction has assets
                if no_assets:
                    imgui.begin_disabled()
                if imgui.button("Sell Asset"):
                    self.state = FactionTurn.TurnFSM.ACTION_SELL_ASSET
                if no_assets:
                    LayoutHelper.add_tooltip("No assets to sell.")
                    imgui.end_disabled()

                if imgui.button("Skip Main Action"):
                    self.state = FactionTurn.TurnFSM.CHECK_GOAL
                LayoutHelper.add_tooltip("Skip the faction's main action this turn.")

            case (
                FactionTurn.TurnFSM.ACTION_ATTACK
                | FactionTurn.TurnFSM.ACTION_MOVE_ASSET
                | FactionTurn.TurnFSM.ACTION_REPAIR_ASSET
                | FactionTurn.TurnFSM.ACTION_EXPAND_INFLUENCE
                | FactionTurn.TurnFSM.ACTION_CREATE_ASSET
                | FactionTurn.TurnFSM.ACTION_HIDE_ASSET
                | FactionTurn.TurnFSM.ACTION_SELL_ASSET
            ):
                self.main_action(factions)

                LayoutHelper.add_spacer()

                if imgui.button(label="Back##Action"):
                    self.state = FactionTurn.TurnFSM.MAIN_ACTION
                if imgui.button(label="Done##Action"):
                    self.state = FactionTurn.TurnFSM.CHECK_GOAL

            case FactionTurn.TurnFSM.CHECK_GOAL:
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
                # Upgrade stats with exp
                imgui.text(f"Faction experience points: {faction.exp}")
                imgui.text(f"CUNNING: {faction.cunning}")
                if faction.cunning < Faction.MAX_ATTRIBUTE:
                    exp_cost = Faction.ATTRIBUTE_COST.get(faction.cunning + 1)
                    disabled = faction.exp < exp_cost
                    if disabled:
                        imgui.begin_disabled()
                    if imgui.button(label=f"Level up ({exp_cost})##Turn_buy_cunning"):
                        faction.exp -= exp_cost
                        faction.cunning += 1
                    if disabled:
                        imgui.end_disabled()
                imgui.text(f"FORCE: {faction.force}")
                if faction.force < Faction.MAX_ATTRIBUTE:
                    exp_cost = Faction.ATTRIBUTE_COST.get(faction.force + 1)
                    disabled = faction.exp < exp_cost
                    if disabled:
                        imgui.begin_disabled()
                    if imgui.button(label=f"Level up ({exp_cost})##Turn_buy_force"):
                        faction.exp -= exp_cost
                        faction.force += 1
                    if disabled:
                        imgui.end_disabled()
                imgui.text(f"WEALTH: {faction.wealth}")
                if faction.wealth < Faction.MAX_ATTRIBUTE:
                    exp_cost = Faction.ATTRIBUTE_COST.get(faction.wealth + 1)
                    disabled = faction.exp < exp_cost
                    if disabled:
                        imgui.begin_disabled()
                    if imgui.button(label=f"Level up ({exp_cost})##Turn_buy_wealth"):
                        faction.exp -= exp_cost
                        faction.wealth += 1
                    if disabled:
                        imgui.end_disabled()
                LayoutHelper.add_spacer()

                if imgui.button("COMPLETE TURN##Turn"):
                    self.state = FactionTurn.TurnFSM.NEXT_FACTION

    def main_action(self: Self, factions: list[Faction]) -> None:
        """Display main action part of statemachine."""
        faction = factions[self.cur_faction]

        # TODO(orkaboy): continue
        match self.state:
            case FactionTurn.TurnFSM.ACTION_ATTACK:
                imgui.text("ATTACK:")
                imgui.text_wrapped(
                    """The faction nominates one or more Assets to attack the enemy in their locations. In each location, the defender chooses which of the Assets present will meet the Attack; thus, if a unit of Infantry attacks in a location where there is an enemy Base of Influence, Informers, and Idealistic Thugs, the defender could decide to use Idealistic Thugs to defend against the attack.
The attacker makes an attribute check based on the attack of the acting Asset; thus, the Infantry would roll Force versus Force. On a success, the defending Asset takes damage equal to the attacking Asset's attack score, or 1d8 in the case of Infantry. On a failure, the attacking Asset takes damage equal to the defending Asset's counterattack score, or 1d6 in the case of Idealistic Thugs.
If the damage done to an Asset reduces it to zero hit points, it is destroyed. The same Asset may be used to defend against multiple attacking Assets, provided it can survive the onslaught.
Damage done to a Base of Influence is also done directly to the faction's hit points. Overflow damage is not transmitted, however; if the Base of Influence only has 5 hit points and 7 hit points are inflicted, the faction loses the Base of Influence and 5 hit points from its total."""  # noqa: E501
                )

                imgui.text(f"{faction} can attack with the following assets:")
                for asset in faction.assets:
                    if asset.is_initialized() and asset.prototype.stats.atk_type:
                        imgui.text(f"{asset} ({asset.loc})")
                        LayoutHelper.add_tooltip(
                            f"{asset.desc}\n\n{asset.prototype.strings.rules}\n\n{asset.prototype.strings.damage_formula}"
                        )
                        # TODO(orkaboy): Automate attack/damage/counter

                if imgui.button("Done attacking##Turn"):
                    self.state = FactionTurn.TurnFSM.CHECK_GOAL

            case FactionTurn.TurnFSM.ACTION_MOVE_ASSET:
                imgui.text("MOVE ASSET:")
                imgui.text_wrapped(
                    """One or more Assets are moved up to one turn's worth of movement each. The receiving location must not have the ability and inclination to forbid the Asset from operating there. Subtle and Stealthed Assets ignore this limit.
If an asset loses the Subtle or Stealth qualities while in a hostile location, they must use this action to retreat to safety within one turn or they will take half their maximum hit points in damage at the start of the next turn, rounded up."""  # noqa: E501
                )

                # TODO(orkaboy): Account for the losing Stealth/Subtle rule?

                imgui.text(f"{faction} can move the following assets:")
                for asset in faction.assets:
                    if asset.is_initialized():
                        imgui.text(f"{asset} ({asset.loc})")
                        LayoutHelper.add_tooltip(f"{asset.desc}\n\n{asset.prototype.strings.rules}")

                        # TODO(orkaboy): Dropdown list and move button for each asset?
                if imgui.button("Done moving assets##Turn"):
                    self.state = FactionTurn.TurnFSM.CHECK_GOAL

            case FactionTurn.TurnFSM.ACTION_REPAIR_ASSET:
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
                if self.repaired_faction:
                    imgui.text("(Repairing faction is only available once per turn)")
                    disabled = True
                if disabled:
                    imgui.begin_disabled()
                if imgui.button("Repair faction"):
                    faction.treasure -= repair_cost
                    faction.hp = min(faction.max_hp(), faction.hp + repair_amount)
                    self.repaired_faction = True
                LayoutHelper.add_tooltip(
                    f"Repair faction for up to {repair_amount} HP, for {repair_cost} Treasure"
                )
                if disabled:
                    imgui.end_disabled()

                if imgui.button("Done repairing##Turn"):
                    self.state = FactionTurn.TurnFSM.CHECK_GOAL

            case FactionTurn.TurnFSM.ACTION_EXPAND_INFLUENCE:
                imgui.text("EXPAND INFLUENCE:")
                imgui.text_wrapped(
                    """The faction seeks to establish a new base of operations in a location. The faction must have at least one Asset there already to make this attempt, and must spend 1 Treasure for each hit point the new Base of Influence is to have. Thus, to create a new Base of Influence with a maximum hit point total of 10, 10 Treasure must be spent. Bases with high maximum hit point totals are harder to dislodge, but losing them also inflicts much more damage on the faction's own hit points.
Once the Base of Influence is created, the owner makes a Cunning versus Cunning attribute check against every other faction that has at least one Asset in the same location. If the other faction wins the check, they are allowed to make an immediate Attack against the new Base of Influence with whatever Assets they have present in the location. The creating faction may attempt to block this action by defending with other Assets present.
If the Base of Influence survives this onslaught, it operates as normal and allows the faction to purchase new Assets there with the Create Asset action."""  # noqa: E501
                )

                locs: set[Location] = {}
                for asset in faction.assets:
                    if asset.loc:
                        locs.add(asset.loc)

                if imgui.begin_combo(label="Base Location##Turn", preview_value=f"{self.boi_loc}"):
                    for loc in locs:
                        _, selected = imgui.selectable(
                            label=f"{loc}##Turn_boi",
                            p_selected=False,
                        )
                        LayoutHelper.add_tooltip(loc.desc)
                        if selected:
                            self.boi_loc = loc
                    imgui.end_combo()
                _, self.boi_hp = imgui.input_int(label="HP##Turn_buy_boi", v=self.boi_hp)

                LayoutHelper.add_spacer()

                if self.boi_loc:
                    imgui.text(
                        f"Build a new base of influence at '{self.boi_loc}' with '{self.boi_hp}' HP (costing {self.boi_hp} Treasure)"  # noqa: E501
                    )

                    # rival_factions: list[str] = []
                    rival_assets: list[Asset] = []
                    faction_assets: list[Asset] = []
                    for asset_cast in self.boi_loc.assets:
                        asset: Asset = asset_cast
                        if asset.is_initialized():
                            if asset.owner != faction.uuid:
                                if asset.prototype.stats.atk_type:
                                    rival_assets.append(asset)
                            else:
                                faction_assets.append(asset)

                    if len(rival_assets) > 0:
                        imgui.text(
                            "The following assets will be able to make a free Attack against the new base if the owning faction succeeds at a Cunning v. Cunning roll:"  # noqa: E501
                        )
                        for asset in rival_assets:
                            owner: Faction = None
                            for faction in factions:
                                if faction.uuid == asset.owner:
                                    owner = faction
                                    break
                            imgui.text(f"{asset} ({owner})")
                            LayoutHelper.add_tooltip(
                                f"{asset.desc}\n\nDamage formula: {asset.prototype.strings.damage_formula}"  # noqa: E501
                            )
                        imgui.text(
                            "The faction building the new base may defend with any assets present:"
                        )
                        for asset in faction_assets:
                            imgui.text(f"{asset}, HP {asset.hp}/{asset.max_hp()}")
                            LayoutHelper.add_tooltip(f"{asset.desc}")

                    disabled = faction.treasure < self.boi_hp
                    if disabled:
                        imgui.begin_disabled()
                    if imgui.button("Build##Turn_buy_boi"):
                        faction.treasure -= self.boi_hp
                        base = BaseOfInfluence(
                            uuid=uuid4().hex,
                            owner=faction.uuid,
                            location=self.boi_loc,
                            max_hp=self.boi_hp,
                        )
                        faction.bases.append(base)
                        self.boi_loc.bases.append(base)
                        # TODO(orkaboy): Cunning v Cunning, Attacks, Defend
                    if disabled:
                        imgui.end_disabled()

                LayoutHelper.add_spacer()

                if imgui.button("Done building bases##Turn"):
                    self.state = FactionTurn.TurnFSM.CHECK_GOAL

            case FactionTurn.TurnFSM.ACTION_CREATE_ASSET:
                imgui.text("CREATE ASSET:")
                imgui.text_wrapped(
                    """The faction buys one Asset at a location where they have a Base of Influence. They must have the minimum attribute and Magic ratings necessary to buy the Asset and must pay the listed cost in Treasure to build it. A faction can create only one Asset per turn.
A faction can have no more Assets of a particular attribute than their attribute score. Thus, a faction with a Force of 3 can have only 3 Force Assets. If this number is exceeded, the faction must pay 1 Treasure per excess Asset at the start of each turn, or else they will lose the excess."""  # noqa: E501
                )
                if imgui.begin_combo(label="Set Goal##Turn", preview_value=f"{self.asset_to_buy}"):
                    imgui.text("=== CUNNING ===")
                    self._create_asset_combo_prototypes(
                        proto_list=cunning_list(), magic=faction.magic, tier=faction.cunning
                    )
                    imgui.text("=== FORCE ===")
                    self._create_asset_combo_prototypes(
                        proto_list=force_list(), magic=faction.magic, tier=faction.force
                    )
                    imgui.text("=== WEALTH ===")
                    self._create_asset_combo_prototypes(
                        proto_list=wealth_list(), magic=faction.magic, tier=faction.wealth
                    )
                    imgui.end_combo()

                if imgui.begin_combo(
                    label="Set Location##Turn", preview_value=f"{self.asset_to_buy_loc}"
                ):
                    for base in faction.bases:
                        _, selected = imgui.selectable(
                            label=f"{base.location}##Turn_buy_loc",
                            p_selected=False,
                        )
                        LayoutHelper.add_tooltip(base.desc)
                        if selected:
                            self.asset_to_buy_loc = base.location
                    imgui.end_combo()
                LayoutHelper.add_spacer()
                if self.asset_to_buy and self.asset_to_buy_loc:
                    cost = self.asset_to_buy.requirements.cost
                    imgui.text(
                        f"Selected asset of type '{self.asset_to_buy}' at location '{self.asset_to_buy_loc}' for {cost} Treasure."  # noqa: E501
                    )
                    can_buy = faction.treasure >= cost
                    if not can_buy:
                        imgui.begin_disabled()
                    if imgui.button(label="Buy Asset##Turn"):
                        faction.treasure -= cost
                        new_asset = Asset(
                            prototype=self.asset_to_buy,
                            owner=faction.uuid,
                            uuid=uuid4().hex,
                            loc=self.asset_to_buy_loc,
                        )
                        faction.assets.append(new_asset)
                        self.asset_to_buy_loc.assets.append(new_asset)
                        self.state = FactionTurn.TurnFSM.CHECK_GOAL
                    if not can_buy:
                        imgui.end_disabled()

            case FactionTurn.TurnFSM.ACTION_HIDE_ASSET:
                imgui.text("HIDE ASSET:")
                imgui.text_wrapped(
                    "An action available only to factions with a Cunning score of 3 or better, this action allows the faction to give one owned Asset the Stealth quality for every 2 Treasure they spend. Assets currently in a location with another faction's Base of Influence can't be hidden. If the Asset later loses the Stealth, no refund is given."  # noqa: E501
                )

                for asset in faction.assets:
                    if not asset.is_initialized() or asset.loc is None:
                        continue

                    if QUALITY.Stealth not in asset.qualities:
                        asset.render_brief()
                        imgui.same_line()
                        # Disable if rival faction has Base of Influence in location
                        rival_at_loc = False
                        for base_cast in asset.loc.bases:
                            base: BaseOfInfluence = base_cast
                            if base.owner != faction.uuid:
                                rival_at_loc = True
                                break

                        disabled = faction.treasure < FactionTurn.HIDE_ACTION_COST or rival_at_loc
                        if disabled:
                            imgui.begin_disabled()
                        if imgui.button(label=f"Add Stealth for 2 Treasure##{asset.uuid}"):
                            faction.treasure -= FactionTurn.HIDE_ACTION_COST
                            asset.qualities.append(QUALITY.Stealth)
                        if disabled:
                            LayoutHelper.add_tooltip("Cannot afford to add Stealth to asset.")
                            imgui.end_disabled()
                if imgui.button("Done hiding##Turn"):
                    self.state = FactionTurn.TurnFSM.CHECK_GOAL

            case FactionTurn.TurnFSM.ACTION_SELL_ASSET:
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
                if imgui.button("Done selling##Turn"):
                    self.state = FactionTurn.TurnFSM.CHECK_GOAL
            case _:
                imgui.text("ERROR STATE")

    def _create_asset_combo_prototypes(
        self: Self, proto_list: list[AssetPrototype], magic: MagicLevel, tier: int
    ) -> None:
        """Fill combo box with assets you are able to buy."""
        for prototype in proto_list:
            if magic < prototype.requirements.magic_level:
                continue
            if tier < prototype.requirements.tier:
                continue
            _, selected = imgui.selectable(
                label=f"{prototype.strings.name}##Turn_buy",
                p_selected=False,
            )
            LayoutHelper.add_tooltip(prototype.strings.rules)
            if selected:
                self.asset_to_buy = prototype

    def execute(self: Self, factions: list[Faction]) -> None:
        """Draw turn logic GUI."""
        imgui.begin("Turn")

        imgui.set_window_pos("Turn", imgui.ImVec2(245, 5), imgui.Cond_.first_use_ever)
        imgui.set_window_size(imgui.ImVec2(240, 410), cond=imgui.Cond_.first_use_ever)

        imgui.text(f"Turn {self.turn_idx}")
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
            self.turn_logic(factions)
            LayoutHelper.add_spacer()
            _, faction.notes = imgui.input_text_multiline(
                label=f"Faction Notes##Turn_{faction.uuid}", str=faction.notes
            )

            # End turn, next faction etc.
            STYLE.button_color(STYLE.COL_RED)
            if imgui.button("Skip faction"):
                self.state = FactionTurn.TurnFSM.NEXT_FACTION
            if imgui.button("Abort Turn"):
                # TODO(orkaboy): Currently doesn't rollback changes made
                self.turn_order = None
                self.state = FactionTurn.TurnFSM.IDLE
            STYLE.pop_color()
        elif imgui.button("New Turn"):
            for faction in factions:
                faction.roll_initiative()
            self.turn_order = sorted(
                factions.copy(), key=lambda faction: faction.initiative, reverse=True
            )
            self.state = FactionTurn.TurnFSM.IDLE
            self.turn_idx += 1

        imgui.end()
