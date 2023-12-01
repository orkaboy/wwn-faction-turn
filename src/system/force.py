from random import randint
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


# TIER 1 FORCE ASSETS
class FearfulIntimidation(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Fearful Intimidation",
                ident="c_fearful_intimidation",
                counter_formula="1d4 damage",
                rules="Judicious exercises of force have intimidated the locals, making them reluctant to cooperate with any group that stands opposed to the faction.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=2,
            ),
            stats=AssetStats(
                max_hp=4,
            ),
        )

    def roll_counter(self: Self) -> int:
        return randint(1, 4)


class LocalGuard(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Local Guard",
                ident="c_local_guard",
                damage_formula="F v. F/1d3+1 damage",
                counter_formula="1d4+1 damage",
                rules="Judicious exercises of force have intimidated the locals, making them reluctant to cooperate with any group that stands opposed to the faction.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=3,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 3) + 1

    def roll_counter(self: Self) -> int:
        return randint(1, 4) + 1


class SummonedHunter(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Summoned Hunter",
                ident="c_summoned_hunter",
                damage_formula="C v. F/1d6 damage",
                rules="A skilled sorcerer has summoned a magical beast or mentally bound a usefully disposable assassin into the faction's service.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                magic_level=MagicLevel.MEDIUM,
                cost=4,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Subtle],
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 6)


class Thugs(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Thugs",
                ident="c_thugs",
                damage_formula="F v. C/1d6 damage",
                rules="These gutter ruffians and common kneebreakers have been organized in service to the faction's causes.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=1,
                cost=2,
            ),
            stats=AssetStats(
                max_hp=1,
                atk_type=AssetType.FORCE,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle],
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 6)


# TIER 2 FORCE ASSETS
class GuerrillaPopulace(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Guerrilla Populace",
                ident="c_guerrilla_populace",
                damage_formula="F v. F/1d4+1 damage",
                rules="The locals have the assistance of trained guerrilla warfare leaders who can aid them in sabotaging and attacking unwary hostiles.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=6,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 4) + 1


class MilitaryTransport(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Military Transport",
                ident="c_military_transport",
                rules="A branch of skilled teamsters, transport ships, road-building crews, or other logistical facilitators is in service to the faction. As a free action once per faction turn, it can bring an allied Asset to its location, provided they're within one turn's movement range, or move an allied Asset from its own location to a target also within a turn's move. Multiple Military Transport assets can chain this movement over long distances.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=4,
            ),
            stats=AssetStats(
                max_hp=6,
                qualities=[QUALITY.Action],
            ),
        )


class ReserveCorps(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Reserve Corps",
                ident="c_reserve_corps",
                damage_formula="F v. F/1d6 damage",
                counter_formula="1d6 damage",
                rules="Retired military personnel and rear-line troops are spread through the area as workers or colonists, available to resist hostilities as needed.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=4,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 6)

    def roll_counter(self: Self) -> int:
        return randint(1, 6)


class Scouts(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Scouts",
                ident="c_scouts",
                damage_formula="F v. F/2d4 damage",
                counter_formula="1d4+1 damage",
                rules="Long-range scouts and reconnaissance experts work for the faction, able to venture deep into hostile territory.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=2,
                cost=5,
            ),
            stats=AssetStats(
                max_hp=5,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Subtle],
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 4) + randint(1, 4)

    def roll_counter(self: Self) -> int:
        return randint(1, 4) + 1


# TIER 3 FORCE ASSETS
class EnchantedElites(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Enchanted Elites",
                ident="c_enchanted_elites",
                damage_formula="F v. F/1d10 damage",
                counter_formula="1d6 damage",
                rules="A carefully-selected group of skilled warriors are given magical armaments and arcane blessings to boost their effectiveness.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=3,
                magic_level=MagicLevel.MEDIUM,
                cost=8,
            ),
            stats=AssetStats(
                max_hp=6,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Subtle],
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 10)

    def roll_counter(self: Self) -> int:
        return randint(1, 6)


class Infantry(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Infantry",
                ident="c_infantry",
                damage_formula="F v. F/1d8 damage",
                counter_formula="1d6 damage",
                rules="Common foot soldiers have been organized and armed by the faction. While rarely particularly heroic in their capabilities, they have the advantage of numbers.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=3,
                cost=6,
            ),
            stats=AssetStats(
                max_hp=6,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 8)

    def roll_counter(self: Self) -> int:
        return randint(1, 6)


class TempleFanatics(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Temple Fanatics",
                ident="c_temple_fanatics",
                damage_formula="F v. F/2d6 damage",
                counter_formula="2d6 damage",
                rules="Fanatical servants of a cult, ideology, or larger religion, these enthusiasts wreak havoc on enemies without a thought for their own lives. After every time the Temple Fanatics defend or successfully attack, they take 1d4 damage.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=3,
                cost=4,
            ),
            stats=AssetStats(
                max_hp=6,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Special],
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 6) + randint(1, 6)

    def roll_counter(self: Self) -> int:
        return randint(1, 6) + randint(1, 6)


class WitchHunters(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Witch Hunters",
                ident="c_witch_hunters",
                damage_formula="C v. C/1d4+1 damage",
                counter_formula="1d6 damage",
                rules="Certain personnel are trained in sniffing out traitors and spies in the organization, along with the presence of hostile magic or hidden spellcraft.",  # noqa: E501
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
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 4) + 1

    def roll_counter(self: Self) -> int:
        return randint(1, 6)


# TIER 4 FORCE ASSETS
class Cavalry(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Cavalry",
                ident="c_cavalry",
                damage_formula="F v. F/2d6 damage",
                counter_formula="1d4 damage",
                rules="Mounted troops, chariots, or other mobile soldiers are in service to the faction. While weak on defense, they can harry logistics and mount powerful charges.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                cost=8,
            ),
            stats=AssetStats(
                max_hp=12,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 6) + randint(1, 6)

    def roll_counter(self: Self) -> int:
        return randint(1, 4)


class MilitaryRoads(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Military Roads",
                ident="c_military_roads",
                rules="The faction has established a network of roads with a logistical stockpile at this Asset's location. As a consequence, once per faction turn, the faction can move any one Asset from any location within its reach to any other location within its reach at a cost of 1 Treasure.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                cost=10,
            ),
            stats=AssetStats(
                max_hp=10,
                qualities=[QUALITY.Action],
            ),
        )


class VanguardUnit(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Vanguard Unit",
                ident="c_vanguard_unit",
                counter_formula="1d6 damage",
                rules="This unit is specially trained to build bridges, reduce fortifications, and facilitate a lightning strike into enemy territory. When its faction takes a Relocate Asset turn, it can move the Vanguard Unit and any allied units at the same location to any other location within range, even if the unit type would normally be prohibitive from moving there. Thus, a Force asset could be moved into a foreign nation's territory even against their wishes. The unit may remain at that location afterwards even if the Vanguard Unit leaves.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                cost=10,
            ),
            stats=AssetStats(
                max_hp=10,
                qualities=[QUALITY.Action],
            ),
        )

    def roll_counter(self: Self) -> int:
        return randint(1, 6)


class WarFleet(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="War Fleet",
                ident="c_war_fleet",
                damage_formula="F v. F/2d6 damage",
                counter_formula="1d8 damage",
                rules="While a war fleet can only Attack assets and locations within reach of the waterways, once per turn it can freely relocate itself to any coastal area within movement range. The Asset itself must be based out of some landward location to provide for supply and refitting.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=4,
                cost=12,
            ),
            stats=AssetStats(
                max_hp=8,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Action],
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 6) + randint(1, 6)

    def roll_counter(self: Self) -> int:
        return randint(1, 8)


# TIER 5 FORCE ASSETS
class DemonicSlayer(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Demonic Slayer",
                ident="c_demonic_slayer",
                damage_formula="C v. C/2d6+2 damage",
                rules="Powerful sorcerers have summoned or constructed an inhuman assassin-beast to hunt down and slaughter the faction's enemies. A Demonic Slayer enters play Stealthed.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=5,
                magic_level=MagicLevel.HIGH,
                cost=12,
            ),
            stats=AssetStats(
                max_hp=4,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.CUNNING,
                qualities=[QUALITY.Subtle, QUALITY.Special, QUALITY.Stealth],
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 6) + randint(1, 6) + 2


class MagicalLogistics(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Magical Logistics",
                ident="c_magical_logistics",
                rules="An advanced web of magical Workings, skilled sorcerers, and trained logistical experts are enlisted to streamline the faction's maintenance and sustain damaged units. Once per faction turn, as a free action, the Asset can repair 2 hit points of damage to an allied Force Asset.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=5,
                magic_level=MagicLevel.MEDIUM,
                cost=14,
            ),
            stats=AssetStats(
                max_hp=6,
                qualities=[QUALITY.Special, QUALITY.Action],
            ),
        )


class SiegeExperts(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Siege Experts",
                ident="c_siege_experts",
                damage_formula="F v. W/1d6 damage",
                counter_formula="1d6 damage",
                rules="These soldiers are trained in trenching, sapping, and razing targeted structures. When they successfully Attack an enemy Asset, the owner loses 1d4 points of Treasure from their reserves and this faction gains it.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=5,
                cost=10,
            ),
            stats=AssetStats(
                max_hp=8,
                atk_type=AssetType.FORCE,
                def_type=AssetType.WEALTH,
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 6)

    def roll_counter(self: Self) -> int:
        return randint(1, 6)


# TIER 6 FORCE ASSETS
class FortificationProgram(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Fortification Program",
                ident="c_fortification_program",
                counter_formula="2d6 damage",
                rules="A program of organized fortification and supply caching has been undertaken around the Asset's location, hardening allied communities and friendly Assets. Once per turn, when an enemy makes an Attack that targets the faction's Force rating, the faction can use the Fortification Program to defend if the Asset is within a turn's move from the attack.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=6,
                cost=20,
            ),
            stats=AssetStats(
                max_hp=18,
                qualities=[QUALITY.Action],
            ),
        )

    def roll_counter(self: Self) -> int:
        return randint(1, 6) + randint(1, 6)


class Knights(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Knights",
                ident="c_knights",
                damage_formula="F v. F/2d8 damage",
                counter_formula="2d6 damage",
                rules="Elite warriors of considerable personal prowess have been trained or enlisted by the faction, either from noble sympathizers, veteran members, or amenable mercenaries.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=6,
                cost=18,
            ),
            stats=AssetStats(
                max_hp=16,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 8) + randint(1, 8)

    def roll_counter(self: Self) -> int:
        return randint(1, 6) + randint(1, 6)


class WarMachines(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="War Machines",
                ident="c_war_machines",
                damage_formula="F v. F/2d10+4 damage",
                counter_formula="1d10 damage",
                rules="Mobile war machines driven by trained beasts or magical motive power are under the faction's control.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=6,
                magic_level=MagicLevel.MEDIUM,
                cost=25,
            ),
            stats=AssetStats(
                max_hp=14,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 10) + randint(1, 10) + 4

    def roll_counter(self: Self) -> int:
        return randint(1, 10)


# TIER 7 FORCE ASSETS
class BrilliantGeneral(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Brilliant General",
                ident="c_brilliant_general",
                damage_formula="C v. F/1d8 damage",
                rules="A leader for the ages is in service with the faction. Whenever the Brilliant General or any allied Force Asset in the same location Attacks or is made to defend, it can roll an extra die to do so.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=7,
                cost=25,
            ),
            stats=AssetStats(
                max_hp=8,
                atk_type=AssetType.CUNNING,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Subtle, QUALITY.Special],
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 8)


class PurityRites(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Purity Rites",
                ident="c_purity_rites",
                counter_formula="2d8+2 damage",
                rules="A rigorous program of regular mental inspection and counterintelligence measures has been undertaken by the faction. This Asset can only defend against attacks that target the faction's Cunning, but it allows the faction to roll an extra die to defend.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=7,
                magic_level=MagicLevel.LOW,
                cost=20,
            ),
            stats=AssetStats(
                max_hp=10,
                qualities=[QUALITY.Special],
            ),
        )

    def roll_counter(self: Self) -> int:
        return randint(1, 8) + randint(1, 8) + 2


class Warshaped(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Warshaped",
                ident="c_warshaped",
                damage_formula="F v. F/2d8+2 damage",
                counter_formula="2d8 damage",
                rules="The faction has the use of magical creatures designed specifically for warfare, or ordinary humans that have been greatly altered to serve the faction's needs. Such forces are few and elusive enough to evade easy detection.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=7,
                magic_level=MagicLevel.HIGH,
                cost=30,
            ),
            stats=AssetStats(
                max_hp=16,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Subtle],
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 8) + randint(1, 8) + 2

    def roll_counter(self: Self) -> int:
        return randint(1, 8) + randint(1, 8)


# TIER 8 FORCE ASSETS
class ApocalypseEngine(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Apocalypse Engine",
                ident="c_apocalypse_engine",
                damage_formula="F v. F/3d10+4 damage",
                rules="One of a number of hideously powerful ancient super-weapons unearthed from some lost armory, an Apocalypse Engine rains some eldritch horror down on a targeted enemy Asset.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=8,
                magic_level=MagicLevel.MEDIUM,
                cost=35,
            ),
            stats=AssetStats(
                max_hp=20,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 10) + randint(1, 10) + randint(1, 10) + 4


class InvincibleLegion(AssetPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            asset_type=AssetType.FORCE,
            strings=AssetStrings(
                name="Invincible Legion",
                ident="c_invincible_legion",
                damage_formula="F v. F/2d10+4 damage",
                counter_formula="2d10+4 damage",
                rules="The faction has developed a truly irresistible military organization that can smash its way through opposition without the aid of any support units. During a Relocate Asset action, the Invincible Legion can relocate to locations that would otherwise not permit a formal military force to relocate there, as if it had the Subtle quality. It is not, however, in any way subtle.",  # noqa: E501
            ),
            requirements=AssetRequirement(
                tier=8,
                cost=40,
            ),
            stats=AssetStats(
                max_hp=30,
                atk_type=AssetType.FORCE,
                def_type=AssetType.FORCE,
                qualities=[QUALITY.Special],
            ),
        )

    def roll_damage(self: Self) -> int:
        return randint(1, 10) + randint(1, 10) + 4

    def roll_counter(self: Self) -> int:
        return randint(1, 10) + randint(1, 10) + 4


class FORCE:
    """Static namespace for Force assets."""

    # TIER 1 FORCE ASSETS
    FearfulIntimidation = FearfulIntimidation()
    LocalGuard = LocalGuard()
    SummonedHunter = SummonedHunter()
    Thugs = Thugs()
    # TIER 2 FORCE ASSETS
    GuerrillaPopulace = GuerrillaPopulace()
    MilitaryTransport = MilitaryTransport()
    ReserveCorps = ReserveCorps()
    Scouts = Scouts()
    # TIER 3 FORCE ASSETS
    EnchantedElites = EnchantedElites()
    Infantry = Infantry()
    TempleFanatics = TempleFanatics()
    WitchHunters = WitchHunters()
    # TIER 4 FORCE ASSETS
    Cavalry = Cavalry()
    MilitaryRoads = MilitaryRoads()
    VanguardUnit = VanguardUnit()
    WarFleet = WarFleet()
    # TIER 5 FORCE ASSETS
    DemonicSlayer = DemonicSlayer()
    MagicalLogistics = MagicalLogistics()
    SiegeExperts = SiegeExperts()
    # TIER 6 FORCE ASSETS
    FortificationProgram = FortificationProgram()
    Knights = Knights()
    WarMachines = WarMachines()
    # TIER 7 FORCE ASSETS
    BrilliantGeneral = BrilliantGeneral()
    PurityRites = PurityRites()
    Warshaped = Warshaped()
    # TIER 8 FORCE ASSETS
    ApocalypseEngine = ApocalypseEngine()
    InvincibleLegion = InvincibleLegion()


_assets = get_class_values(FORCE)


def force_list() -> list[AssetPrototype]:
    """Return list of all Force Assets."""
    return _assets
