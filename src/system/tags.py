from typing import Self

from src.mapper import get_class_values


class TagPrototype:
    def __init__(self: Self, ident: str, name: str, rules: str) -> None:
        """Initialize TagPrototype object."""
        self.id = ident
        self.name = name
        self.rules = rules


class Antimagical(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_antimagical",
            name="Antimagical",
            rules="The faction is dwarven or of some other breed of skilled counter-sorcerers. Assets that require Medium or higher Magic to purchase roll all attribute checks twice against this faction during an Attack and take the worst roll.",  # noqa: E501
        )


class Concealed(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_concealed",
            name="Concealed",
            rules="All Assets the faction purchases enter play with the Stealth quality.",
        )


class Imperialist(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_imperialist",
            name="Imperialist",
            rules="The faction quickly expands its Bases of Influence. Once per turn, it can use the Expand Influence action as a special ability instead of it taking a full action.",  # noqa: E501
        )


class Innovative(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_innovative",
            name="Innovative",
            rules="The faction can purchase Assets as if their attribute ratings were two points higher than they are. Only two such over-complex Assets may be owned at any one time.",  # noqa: E501
        )


class Machiavellian(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_machiavellian",
            name="Machiavellian",
            rules="The faction is diabolically cunning. It rolls an extra die for all Cunning attribute checks. Its Cunning must always be its highest attribute.",  # noqa: E501
        )


class Martial(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_martial",
            name="Martial",
            rules="The faction is profoundly devoted to war. It rolls an extra die for all Force attribute checks. Force must always be its highest attribute.",  # noqa: E501
        )


class Massive(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_massive",
            name="Massive",
            rules="he faction is an empire, major kingdom, or other huge organizational edifice. It automatically wins attribute checks if its attribute is more than twice as big as the opposing side’s attribute, unless the other side is also Massive.",  # noqa: E501
        )


class Mobile(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_mobile",
            name="Mobile",
            rules="The faction is exceptionally fast or mobile. Its faction turn movement range is twice what another faction would have in the same situation.",  # noqa: E501
        )


class Populist(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_populist",
            name="Populist",
            rules="The faction has widespread popular support. Assets that cost 5 Treasure or less to buy cost one point less, to a minimum of 1.",  # noqa: E501
        )


class Rich(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_rich",
            name="Rich",
            rules="The faction is rich or possessed of mercantile skill. It rolls an extra die for all Wealth attribute checks. Wealth must always be its highest attribute.",  # noqa: E501
        )


class Rooted(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_rooted",
            name="Rooted",
            rules="The faction has very deep roots in its area of influence. They roll an extra die for attribute checks in their headquarters location, and all rivals roll their own checks there twice, taking the worst die.",  # noqa: E501
        )


class Scavenger(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_scavenger",
            name="Scavenger",
            rules="As looters and raiders, when they destroy an enemy Asset they gain a quarter of its purchase value in Treasure, rounded up.",  # noqa: E501
        )


class Supported(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_supported",
            name="Supported",
            rules="The faction has excellent logistical support. All damaged Assets except Bases of Influence regain one lost hit point per faction turn automatically.",  # noqa: E501
        )


class Tenacious(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_tenacious",
            name="Tenacious",
            rules="The faction is hard to dislodge. When one of its Bases of Influence is reduced to zero hit points, it instead survives with 1 hit point. This trait can’t be used again on that base until it’s fully fixed.",  # noqa: E501
        )


class Zealot(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_zealot",
            name="Zealot",
            rules="Once per turn, when an Asset fails an Attack action check, it can reroll the attribute check. It automatically takes counterattack damage from its target, however, or 1d6 if the target has less or none.",  # noqa: E501
        )


class TAGS:
    """Static namespace for Tags."""

    Antimagical = Antimagical()
    Concealed = Concealed()
    Imperialist = Imperialist()
    Innovative = Innovative()
    Machiavellian = Machiavellian()
    Martial = Martial()
    Massive = Massive()
    Mobile = Mobile()
    Populist = Populist()
    Rich = Rich()
    Rooted = Rooted()
    Scavenger = Scavenger()
    Supported = Supported()
    Tenacious = Tenacious()
    Zealot = Zealot()


_tags = get_class_values(TAGS)


def tags_list() -> list[TagPrototype]:
    """Return list of all Tags."""
    return _tags
