from typing import Self

from src.mapper import get_class_values
from src.system.asset_proto import (
    AssetPrototype,
    AssetRequirement,
    AssetStats,
    AssetStrings,
    AssetType,
    MagicLevel,
)
from src.system.qualities import QUALITY


# TIER 1 WEALTH ASSETS
class ArmedGuards(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Armed Guards",
                ident="c_armed_guards",
                damage_formula="W v. F/1d3 damage",
                counter_formula="1d4 damage",
                rules="Hired caravan guards, bodyguards, or other armed minions serve the faction.",
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=1,
            ),
            stats=AssetStats(
                max_hp=3,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.FORCE,
            ),
        )


class CooperativeBusinesses(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Cooperative Businesses",
                ident="c_cooperative_businesses",
                damage_formula="W v. W/1d4-1 damage",
                rules="If any other faction attempts to create an Asset in the same location as a Cooperative Business, the cost of doing so increases by 1 Treasure. This penalty stacks.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=1,
            ),
            stats=AssetStats(
                max_hp=2,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


class Farmers(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Farmers",
                ident="c_farmers",
                counter_formula="1d4 damage",
                rules="Farmers, hunters, and simple rural artisans are in service to the faction here. Once per turn, as a free action, the Asset's owner can roll 1d6; on a 5+, they gain 1 Treasure from the Farmers.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=2,
            ),
            stats=AssetStats(
                max_hp=4,
                qualities=[QUALITY.Action],
            ),
        )


class FrontMerchant(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Front Merchant",
                ident="c_front_merchant",
                damage_formula="W v. W/1d4 damage",
                counter_formula="1d4-1 damage",
                rules="Whenever the Front Merchant successfully Attacks an enemy Asset, the target faction loses 1 Treasure, if they have any, and the Front Merchant's owner gains it. Such a loss can occur only once per turn.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=2,
            ),
            stats=AssetStats(
                max_hp=3,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Subtle],
            ),
        )


# TIER 2 WEALTH ASSETS
class Caravan(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Caravan",
                ident="c_caravan",
                damage_formula="W v. W/1d4 damage",
                rules="As a free action, once per turn, the Caravan can spend 1 Treasure and move itself and one other Asset in the same place to a new location within one move.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=5,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Action],
            ),
        )


class Dragomans(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Dragomans",
                ident="c_dragomans",
                counter_formula="1d4 damage",
                rules="Interpreters, cultural specialists, and go-betweens simplify the expansion of a faction's influence in an area. A faction that takes an Expand Influence action in the same location as this Asset can roll an extra die on all checks there that turn. As a free action once per turn, this Asset can move.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=4,
            ),
            stats=AssetStats(
                max_hp=4,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


class Pleaders(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Pleaders",
                ident="c_pleaders",
                damage_formula="C v. W/2d4 damage",
                counter_formula="1d6 damage",
                rules="Whether lawyers, skalds, lawspeakers, sage elders, or other legal specialists, Pleaders can turn the local society's laws against the enemies of the faction. However, Pleaders can neither Attack nor inflict Counterattack damage on Force Assets.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=6,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Special],
            ),
        )


class WorkerMob(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Worker Mob",
                ident="c_worker_mob",
                damage_formula="W v. F/1d4+1 damage",
                counter_formula="1d4 damage",
                rules="The roughest, most brutal laborers in service with the faction have been quietly organized to sternly discipline the enemies of the group.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=4,
            ),
            stats=AssetStats(
                max_hp=6,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.FORCE,
            ),
        )


# TIER 3 WEALTH ASSETS
class AncientMechanisms(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Ancient Mechanisms",
                ident="c_ancient_mechanisms",
                rules="Some useful magical mechanism from ages past has been refitted to be useful in local industry. Whenever an Asset in the same location must roll to make a profit, such as Farmers or Manufactory, the faction may roll the die twice and take the better result.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=3,
                magic_level=MagicLevel.MEDIUM,
                cost=8,
            ),
            stats=AssetStats(
                max_hp=4,
                qualities=[QUALITY.Special],
            ),
        )


class ArcaneLaboratory(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Arcane Laboratory",
                ident="c_arcane_laboratory",
                rules="The faction's overall Magic is counted as one step higher for the purposes of creating Assets in the same location as the laboratory. Multiple Arcane Laboratories in the same location can increase the Magic boost by multiple steps.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=3,
                cost=6,
            ),
            stats=AssetStats(
                max_hp=4,
                qualities=[QUALITY.Special],
            ),
        )


class FreeCompany(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Free Company",
                ident="c_free_company",
                damage_formula="W v. F/2d4+2 damage",
                counter_formula="1d6 damage",
                rules="Hired mercenaries and professional soldiers, this Asset can, as a free action once per turn, move itself. At the start of each of its owner's turn, it takes 1 Treasure in upkeep costs; if this is not paid, roll 1d6. On a 1-3 the Asset is lost, on a 4-6 it goes rogue and will move to Attack the most profitable-looking target. This roll is repeated each turn until back pay is paid or the Asset is lost.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=3,
                cost=8,
            ),
            stats=AssetStats(
                max_hp=6,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Action, QUALITY.Special],
            ),
        )


class Manufactory(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Manufactory",
                ident="c_manufactory",
                counter_formula="1d4 damage",
                rules="Once per turn, as a free action, the Asset's owner may roll 1d6; on a 1, one point of Treasure is lost, on a 2-5, one point is gained, and on a 6, two points are gained. If Treasure is lost and none is available to pay it by the end of the turn, this Asset is lost.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=3,
                cost=8,
            ),
            stats=AssetStats(
                max_hp=4,
                qualities=[QUALITY.Action],
            ),
        )


# TIER 4 WEALTH ASSETS
class Healers(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Healers",
                ident="c_healers",
                rules="Whenever an Asset within one move of the Healers is destroyed by an Attack that used Force against the target, the owner of the Healers may pay half its purchase price in Treasure, rounded up, to instantly restore it with 1 hit point. This cannot be used to repair Bases of Influence.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                cost=12,
            ),
            stats=AssetStats(
                max_hp=8,
                qualities=[QUALITY.Action],
            ),
        )


class Monopoly(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Monopoly",
                ident="c_monopoly",
                damage_formula="W v. W/1d6 damage",
                counter_formula="1d6 damage",
                rules="Once per turn, as a free action, the Monopoly Asset can target an Asset in the same location; that Asset's owning faction must either pay the Monopoly's owner 1 Treasure or lose the targeted Asset.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                cost=8,
            ),
            stats=AssetStats(
                max_hp=12,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Action],
            ),
        )


class OccultCountermeasures(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Occult Countermeasures",
                ident="c_occult_countermeasures",
                damage_formula="W v. C/2d10 damage",
                counter_formula="1d10 damage",
                rules="This asset can only Attack or inflict Counterattack damage on Assets that require at least a Low Magic rating to purchase.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                magic_level=MagicLevel.LOW,
                cost=10,
            ),
            stats=AssetStats(
                max_hp=8,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Special],
            ),
        )


class Usurers(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Usurers",
                ident="c_usurers",
                damage_formula="W v. W/1d10 damage",
                rules="Moneylenders and other proto-bankers ply their trade for the faction. For each unit of Usurers owned by a faction, the Treasure cost of buying Assets may be decreased by 2 Treasure, to a minimum of half its cost. Each time the Usurers are used for this benefit, they suffer 1d4 damage from popular displeasure.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                cost=12,
            ),
            stats=AssetStats(
                max_hp=8,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Action],
            ),
        )


# TIER 5 WEALTH ASSETS
class MadGenius(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Mad Genius",
                ident="c_mad_genius",
                damage_formula="W v. C/1d6 damage",
                rules="As a free action, once per turn, the Mad Genius may move. As a free action, once per turn, the Mad Genius may be sacrificed to treat the Magic rating in their location as High for the purpose of buying Assets that require such resources. This boost lasts only until the next Asset is purchased in that location.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=5,
                cost=6,
            ),
            stats=AssetStats(
                max_hp=2,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Action],
            ),
        )


class SmugglingFleet(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Smuggling Fleet",
                ident="c_smuggling_fleet",
                damage_formula="W v. F/2d6 damage",
                rules="Once per turn, as a free action, they may move themselves and any one Asset at their current location to any other water-accessible location within one move. Any Asset they move with them gains the Subtle quality until they take some action at the destination.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=5,
                cost=12,
            ),
            stats=AssetStats(
                max_hp=6,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Subtle, QUALITY.Action],
            ),
        )


class SupplyInterruption(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Supply Interruption",
                ident="c_supply_interruption",
                damage_formula="C v. W/1d6 damage",
                rules="As a free action, once per turn, the Asset can make a Cunning vs. Wealth check against an Asset in the same location. On a success, the owning faction must sacrifice Treasure equal to half the target Asset's purchase cost, or else it is disabled and useless until this price is paid.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=5,
                cost=10,
            ),
            stats=AssetStats(
                max_hp=8,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Subtle, QUALITY.Action],
            ),
        )


# TIER 6 WEALTH ASSETS
class EconomicDisruption(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Economic Disruption",
                ident="c_economic_disruption",
                damage_formula="W v. W/2d6 damage",
                rules="As a free action once per turn, this Asset can move itself without cost.",
            ),
            requirements=AssetRequirement(
                tier=6,
                cost=25,
            ),
            stats=AssetStats(
                max_hp=10,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Subtle, QUALITY.Action],
            ),
        )


class MerchantPrince(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Merchant Prince",
                ident="c_merchant_prince",
                damage_formula="W v. W/2d8 damage",
                counter_formula="1d8 damage",
                rules="A canny master of trade, the Merchant Prince may be triggered as a free action once per turn before buying a new Asset in the same location; the Merchant Prince takes 1d4 damage and the purchased Asset costs 1d8 Treasure less, down to a minimum of half its normal price.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=6,
                cost=20,
            ),
            stats=AssetStats(
                max_hp=10,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Action],
            ),
        )


class TradeCompany(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Trade Company",
                ident="c_trade_company",
                damage_formula="W v. W/2d6 damage",
                counter_formula="1d6 damage",
                rules="Bold traders undertake potentially lucrative- or catastrophic- new business opportunities. As a free action, once per turn, the owner of the Asset may roll accept 1d4 damage done to the Asset in exchange for earning 1d6-1 Treasure points.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=6,
                cost=15,
            ),
            stats=AssetStats(
                max_hp=10,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Action],
            ),
        )


# TIER 7 WEALTH ASSETS
class AncientWorkshop(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Ancient Workshop",
                ident="c_ancient_workshop",
                rules="A workshop has been refitted with ancient magical tools, allowing prodigies of production, albeit not always safely. As a free action, once per turn, the Ancient Workshop takes 1d6 damage and the owning faction gains 1d6 Treasure.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=7,
                magic_level=MagicLevel.MEDIUM,
                cost=25,
            ),
            stats=AssetStats(
                max_hp=16,
                qualities=[QUALITY.Action],
            ),
        )


class LeadOrSilver(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Lead or Silver",
                ident="c_lead_or_silver",
                damage_formula="W v. W/2d10 damage",
                counter_formula="2d8 damage",
                rules="If Lead or Silver's Attack reduces an enemy Asset to zero hit points, this Asset's owner may immediately pay half the target's purchase cost to claim it as their own, reviving it with 1 hit point.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=7,
                cost=20,
            ),
            stats=AssetStats(
                max_hp=10,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Special],
            ),
        )


class TransportNetwork(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="TransportNetwork",
                ident="c_transport_network",
                damage_formula="W v. W/1d12 damage",
                rules="A vast array of carters, ships, smugglers, and official caravans are under the faction's control. As a free action the Transport Network can spend 1 Treasure to move any friendly Asset within two moves to any location within one move of either the target or the Transport Network.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=7,
                cost=15,
            ),
            stats=AssetStats(
                max_hp=5,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Action],
            ),
        )


# TIER 8 WEALTH ASSETS
class GoldenProsperity(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Golden Prosperity",
                ident="c_golden_prosperity",
                counter_formula="2d10 damage",
                rules="Each turn, as a free action, the faction gains 1d6 Treasure that can be used to fix damaged Assets as if by the Repair Assets action. Any of this Treasure not spent on such purposes is lost.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=8,
                magic_level=MagicLevel.MEDIUM,
                cost=40,
            ),
            stats=AssetStats(
                max_hp=30,
                qualities=[QUALITY.Action],
            ),
        )


class HiredLegion(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.WEALTH,
            strings=AssetStrings(
                name="Hired Legion",
                ident="c_hired_legion",
                damage_formula="W v F/2d10+4 damage",
                counter_formula="2d10 damage",
                rules="As a free action once per turn, the Hired Legion can move. This faction must be paid 2 Treasure at the start of each turn as upkeep, or else they go rogue as the Free Company Asset does. This Asset cannot be voluntarily sold or disbanded.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=8,
                cost=30,
            ),
            stats=AssetStats(
                max_hp=20,
                atk_type=AssetType.WEALTH,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Action],
            ),
        )


class WEALTH:
    """Static namespace for Wealth assets."""

    # TIER 1 WEALTH ASSETS
    ArmedGuards = ArmedGuards()
    CooperativeBusinesses = CooperativeBusinesses()
    Farmers = Farmers()
    FrontMerchant = FrontMerchant()
    # TIER 2 WEALTH ASSETS
    Caravan = Caravan()
    Dragomans = Dragomans()
    Pleaders = Pleaders()
    WorkerMob = WorkerMob()
    # TIER 3 WEALTH ASSETS
    AncientMechanisms = AncientMechanisms()
    ArcaneLaboratory = ArcaneLaboratory()
    FreeCompany = FreeCompany()
    Manufactory = Manufactory()
    # TIER 4 WEALTH ASSETS
    Healers = Healers()
    Monopoly = Monopoly()
    OccultCountermeasures = OccultCountermeasures()
    Usurers = Usurers()
    # TIER 5 WEALTH ASSETS
    MadGenius = MadGenius()
    SmugglingFleet = SmugglingFleet()
    SupplyInterruption = SupplyInterruption()
    # TIER 6 WEALTH ASSETS
    EconomicDisruption = EconomicDisruption()
    MerchantPrince = MerchantPrince()
    TradeCompany = TradeCompany()
    # TIER 7 WEALTH ASSETS
    AncientWorkshop = AncientWorkshop()
    LeadOrSilver = LeadOrSilver()
    TransportNetwork = TransportNetwork()
    # TIER 8 WEALTH ASSETS
    GoldenProsperity = GoldenProsperity()
    HiredLegion = HiredLegion()


_assets = get_class_values(WEALTH)


def wealth_list() -> list[AssetPrototype]:
    """Return list of all Wealth Assets."""
    return _assets
