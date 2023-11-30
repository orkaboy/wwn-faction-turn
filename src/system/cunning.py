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


# TIER 1 CUNNING ASSETS
class Informers(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Informers",
                ident="c_informers",
                damage_formula="C v. C/Special",
                rules="As a free action, once per turn, the faction can spend 1 Treasure and have the Informers look for Stealthed Assets. To do so, the Informers pick a faction and make a Cunning vs. Cunning Attack on them. No counterattack damage is taken if they fail, but if they succeed, all Stealthed Assets of that faction within one move of the Informers are revealed",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=2,
            ),
            stats=AssetStats(
                max_hp=3,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle, QUALITY.Special, QUALITY.Action],
            ),
        )


class PettySeers(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Petty Seers",
                ident="c_petty_seers",
                counter_formula="1d6 damage",
                rules="A cadre of skilled fortune-tellers and minor oracles have been enlisted by the faction to foresee perils and allow swift counterattacks.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=2,
                magic_level=MagicLevel.MEDIUM,
            ),
            stats=AssetStats(
                max_hp=2,
                qualities=[QUALITY.Subtle],
            ),
        )


class Smugglers(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Smugglers",
                ident="c_smugglers",
                damage_formula="C v. W/1d4 damage",
                rules="As a free action, once per faction turn, the Smugglers can move any allied Wealth or Cunning Asset in their same location to a destination within movement range, even if the destination wouldn't normally allow an un-Subtle Asset to locate there.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=2,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Subtle, QUALITY.Action],
            ),
        )


class UsefulIdiots(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Useful Idiots",
                ident="c_useful_idiots",
                rules="Hirelings, catspaws, foolish idealists, and other disposable minions are gathered together in this Asset. If another Asset within one turn's move of the Useful Idiots is struck by an Attack, the faction can instead sacrifice the Useful Idiots to negate the attack. Only one band of Useful Idiots can be sacrificed on any one turn.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=1,
            ),
            stats=AssetStats(
                max_hp=2,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


# TIER 2 CUNNING ASSETS
class Blackmail(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Blackmail",
                ident="c_blackmail",
                damage_formula="C v. C/1d4 damage",
                rules="When a Blackmail asset is in a location, hostile factions can't roll more than one die during Attacks made by or against them there, even if they have tags or Assets that usually grant bonus dice.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=4,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


class DancingGirls(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Dancing Girls",
                ident="c_dancing_girls",
                damage_formula="C v. W/2d4 damage",
                rules="Dancing Girls or other charming distractions are immune to Attack or Counterattack damage from Force Assets, but they cannot be used to defend against Attacks from Force Assets.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=4,
            ),
            stats=AssetStats(
                max_hp=3,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


class HiredFriends(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Hired Friends",
                ident="c_hired_friends",
                damage_formula="C v. C/1d6 damage",
                rules="As a free action, once per turn, the faction may spend 1 Treasure and grant a Wealth Asset within one turn's movement range the Subtle quality. This quality will remain, regardless of the Wealth Asset's movement, until the Hired Friends are destroyed or they use this ability again.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=4,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle, QUALITY.Special, QUALITY.Action],
            ),
        )


class Saboteurs(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Saboteurs",
                ident="c_saboteurs",
                damage_formula="C v. W/2d4 damage",
                rules="An Asset that is Attacked by the Saboteurs can't use any free action abilities it may have during the next turn, whether or not the Attack was successful.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=5,
            ),
            stats=AssetStats(
                max_hp=6,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.WEALTH,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


# TIER 3 CUNNING ASSETS
class BewitchingCharmer(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Bewitching Charmer",
                ident="c_bewitching_charmer",
                damage_formula="C v. C/Special",
                rules="When the Bewitching Charmer succeeds in an Attack, the targeted Asset is unable to leave the same location as the Bewitching Charmer until the latter Asset moves or is destroyed. Bewitching Charmers are immune to Counterattack.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=3,
                magic_level=MagicLevel.LOW,
                cost=6,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


class CovertTransport(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Covert Transport",
                ident="c_covert_transport",
                rules="As a free action once per turn, the faction can pay 1 Treasure and move any Cunning or Wealth Asset at the same location as the Covert Transport. The transported Asset gains the Stealth quality until it performs some action or is otherwise utilized by the faction.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=3,
                cost=8,
            ),
            stats=AssetStats(
                max_hp=4,
                qualities=[QUALITY.Subtle, QUALITY.Special, QUALITY.Action],
            ),
        )


class OccultInfiltrators(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Occult Infiltrators",
                ident="c_occult_infiltrators",
                damage_formula="C v. C/2d6 damage",
                rules="Magically-gifted spies and assassins are enlisted to serve the faction. Occult Infiltrator Assets always begin play with the Stealth quality.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=3,
                magic_level=MagicLevel.MEDIUM,
                cost=6,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


class Spymaster(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Spymaster",
                ident="c_spymaster",
                damage_formula="C v. C/1d6 damage",
                counter_formula="2d6 damage",
                rules="A veteran operative runs a counterintelligence bureau in the area and formulates offensive schemes for the faction.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=3,
                cost=8,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle],
            ),
        )


# TIER 4 CUNNING ASSETS
class CourtPatronage(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Court Patronage",
                ident="c_court_patronage",
                damage_formula="C v. C/1d6 damage",
                counter_formula="1d6 damage",
                rules="Powerful nobles or officials are appointing their agents to useful posts of profit. A Court Patronage Asset automatically grants 1 Treasure to its owning faction each turn.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                cost=8,
            ),
            stats=AssetStats(
                max_hp=8,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


class IdealisticThugs(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Idealistic Thugs",
                ident="c_idealistic_thugs",
                damage_formula="C v. F/1d6 damage",
                counter_formula="1d6 damage",
                rules="Easily-manipulated hotheads are enlisted under whatever ideological or religious principle best enthuses them for violence.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                cost=8,
            ),
            stats=AssetStats(
                max_hp=12,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Subtle],
            ),
        )


class Seditionists(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Seditionists",
                ident="c_seditionists",
                damage_formula="Special",
                rules="In place of an Attack action, the Seditionists' owners may spend 1d4 Treasure and attach the Asset to a hostile Asset in the same location. Until the Seditionists are destroyed, infest another Asset, or leave the same location, the rebelling Asset cannot be used for anything and grants no benefits.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                cost=12,
            ),
            stats=AssetStats(
                max_hp=8,
                qualities=[QUALITY.Subtle],
            ),
        )


class VigilantAgents(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Vigilant Agents",
                ident="c_vigilant_agents",
                counter_formula="1d4 damage",
                rules="A constant flow of observations runs back to the faction from these watchful counterintelligence agents. Whenever another faction moves a Stealthed asset into a location within one move's distance from the Vigilant Agents, they may make a Cunning vs. Cunning attack against the owning faction. On a success, the intruding Asset loses its Stealth after it completes the move.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                cost=12,
            ),
            stats=AssetStats(
                max_hp=8,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


# TIER 5 CUNNING ASSETS
class Cryptomancers(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Cryptomancers",
                ident="c_cryptomancers",
                damage_formula="C v. C/Special",
                rules="In place of an Attack action, they can make a Cunning vs. Cunning attack on a specific hostile Asset within one move. On a success, the targeted Asset is unable to do anything or be used for anything on its owner's next faction turn. On a failure, no Counterattack damage is taken.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=5,
                magic_level=MagicLevel.LOW,
                cost=14,
            ),
            stats=AssetStats(
                max_hp=6,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle],
            ),
        )


class OrganizationMoles(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Organization Moles",
                ident="c_organization_moles",
                damage_formula="C v. C/2d6 damage",
                rules="Sleeper agents and deep-cover spies burrow into hostile organizations, waiting to disrupt them from within when ordered to do so.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=5,
                cost=8,
            ),
            stats=AssetStats(
                max_hp=10,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle],
            ),
        )


class Shapeshifters(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Shapeshifters",
                ident="c_shapeshifters",
                damage_formula="C v. C/2d6 damage",
                rules="As a free action once per turn, the faction can spend 1 Treasure and grant the Shapeshifters the Stealth quality.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=5,
                magic_level=MagicLevel.MEDIUM,
                cost=14,
            ),
            stats=AssetStats(
                max_hp=8,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle, QUALITY.Special, QUALITY.Action],
            ),
        )


# TIER 6 CUNNING ASSETS
class InterruptedLogistics(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Interrupted Logistics",
                ident="c_interrupted_logistics",
                rules="Non-Stealthed hostile units cannot enter the same location as the Interrupted Logistics Asset without paying 1d4 Treasure and waiting one turn to arrive there.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=6,
                cost=20,
            ),
            stats=AssetStats(
                max_hp=10,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


class Prophet(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Prophet",
                ident="c_prophet",
                damage_formula="C v. C/2d8 damage",
                counter_formula="1d8 damage",
                rules="Whether a religious prophet, charismatic philosopher, rebel leader, or other figure of popular appeal, the Asset is firmly under the faction's control.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=6,
                cost=20,
            ),
            stats=AssetStats(
                max_hp=10,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle],
            ),
        )


class UndergroundRoads(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Underground Roads",
                ident="c_underground_roads",
                rules="A well-established network of secret transit extends far around this Asset. As a free action, the faction may pay 1 Treasure and move any friendly Asset from a location within one round's move of the Underground Roads to a destination also within one round's move of the Roads.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=6,
                cost=18,
            ),
            stats=AssetStats(
                max_hp=15,
                qualities=[QUALITY.Subtle, QUALITY.Special, QUALITY.Action],
            ),
        )


# TIER 7 CUNNING ASSETS
class ExpertTreachery(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Expert Treachery",
                ident="c_expert_treachery",
                damage_formula="C v. C/Special",
                rules="On a successful Attack by Expert Treachery, this Asset is lost, 5 Treasure is gained by its owning faction, and the Asset that Expert Treachery targeted switches sides. This conversion happens even if their new owners lack the attributes usually necessary to maintain their new Asset.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=7,
                cost=10,
            ),
            stats=AssetStats(
                max_hp=5,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle],
            ),
        )


class Mindbenders(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Mindbenders",
                ident="c_mindbenders",
                counter_formula="2d8 damage",
                rules="Once per turn as a free action, the Mindbenders can force a rival faction to reroll a check, Attack, or other die roll they just made and take whichever result the Mindbenders prefer. A faction can only be affected this way once until the start of the Mindbender's faction's next turn.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=7,
                magic_level=MagicLevel.MEDIUM,
                cost=20,
            ),
            stats=AssetStats(
                max_hp=10,
                qualities=[QUALITY.Subtle, QUALITY.Action],
            ),
        )


class PopularMovement(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Popular Movement",
                ident="c_popular_movement",
                damage_formula="C v. C/2d6 damage",
                counter_formula="1d6 damage",
                rules="Any friendly Asset is allowed movement into the same location as the Popular Movement, even if it would normally be forbidden by its owners and lacks the Subtle quality. If the Popular Movement later moves or is destroyed, such Assets must also leave or suffer the usual consequences of a non-Subtle Asset in a hostile area.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=7,
                cost=25,
            ),
            stats=AssetStats(
                max_hp=16,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


# TIER 8 CUNNING ASSETS
class JustAsPlanned(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Just As Planned",
                ident="c_just_as_planned",
                counter_formula="1d10 damage",
                rules="Some sublimely cunning mastermind ensures that the schemes of this faction are unimaginably subtle and far-seeing. Whenever the faction's Assets make a roll involving Cunning, they may reroll a failed check at the cost of inflicting 1d6 damage on Just As Planned. This may be done repeatedly, though it may destroy the Asset. There is no range limit on this benefit.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=8,
                cost=40,
            ),
            stats=AssetStats(
                max_hp=15,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


class OmniscientSeers(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.CUNNING,
            strings=AssetStrings(
                name="Omniscient Seers",
                ident="c_omniscient_seers",
                counter_formula="1d8 damage",
                rules="At the start of their turn, each hostile Stealthed asset within one turn's movement of the Omniscient Seers must succeed in a Cunning vs. Cunning check against the owning faction or lose their Stealth. In addition, all Cunning rolls made by the faction for units or events within one turn's movement of the seers gain an extra die.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=8,
                magic_level=MagicLevel.HIGH,
                cost=30,
            ),
            stats=AssetStats(
                max_hp=10,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )


class CUNNING:
    """Static namespace for Cunning asset prototypes."""

    # TIER 1 CUNNING ASSETS
    Informers = Informers()
    PettySeers = PettySeers()
    Smugglers = Smugglers()
    UsefulIdiots = UsefulIdiots()
    # TIER 2 CUNNING ASSETS
    Blackmail = Blackmail()
    DancingGirls = DancingGirls()
    HiredFriends = HiredFriends()
    Saboteurs = Saboteurs()
    # TIER 3 CUNNING ASSETS
    BewitchingCharmer = BewitchingCharmer()
    CovertTransport = CovertTransport()
    OccultInfiltrators = OccultInfiltrators()
    Spymaster = Spymaster()
    # TIER 4 CUNNING ASSETS
    CourtPatronage = CourtPatronage()
    IdealisticThugs = IdealisticThugs()
    Seditionists = Seditionists()
    VigilantAgents = VigilantAgents()
    # TIER 5 CUNNING ASSETS
    Cryptomancers = Cryptomancers()
    OrganizationMoles = OrganizationMoles()
    Shapeshifters = Shapeshifters()
    # TIER 6 CUNNING ASSETS
    InterruptedLogistics = InterruptedLogistics()
    Prophet = Prophet()
    UndergroundRoads = UndergroundRoads()
    # TIER 7 CUNNING ASSETS
    ExpertTreachery = ExpertTreachery()
    Mindbenders = Mindbenders()
    PopularMovement = PopularMovement()
    # TIER 8 CUNNING ASSETS
    JustAsPlanned = JustAsPlanned()
    OmniscientSeers = OmniscientSeers()


_assets = get_class_values(CUNNING)


def cunning_list() -> list[AssetPrototype]:
    """Return list of all Cunning Assets."""
    return _assets
