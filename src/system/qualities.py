from typing import Self

from src.mapper import get_class_values
from src.quality import Quality


class Stealth(Quality):
    def __init__(self: Self) -> None:
        super().__init__(
            name="Stealth",
            ident="q_stealth",
            rules="Assets with the Stealth quality can move freely to any location within reach. Stealthed Assets cannot be Attacked by other Assets until they lose the Stealth quality. This happens when they are discovered by certain special Assets or when the Stealthed Asset Attacks something.",  # noqa: E501
            persistent=False,
        )


class Subtle(Quality):
    def __init__(self: Self) -> None:
        super().__init__(
            name="Subtle",
            ident="q_subtle",
            rules="Subtle Assets can move to locations even where they would normally be prohibited by the ruling powers. Dislodging them requires that they be Attacked until destroyed or moved out by their owner.",  # noqa: E501
        )


class Special(Quality):
    def __init__(self: Self) -> None:
        super().__init__(
            name="Special",
            ident="q_special",
            rules="The Asset posseses some special rules.",
        )


class Action(Quality):
    def __init__(self: Self) -> None:
        super().__init__(
            name="Action",
            ident="q_action",
            rules="The Asset grants a free Action.",
        )


class QUALITY:
    """Static namespace for Qualities."""

    Action = Action()
    Special = Special()
    Stealth = Stealth()
    Subtle = Subtle()


_quality = get_class_values(QUALITY)


def quality_list() -> list[QUALITY]:
    return _quality
