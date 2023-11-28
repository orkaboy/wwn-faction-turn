from typing import Self

from src.tag import TagPrototype


class Antimagical(TagPrototype):
    def __init__(self: Self) -> None:
        super().__init__(
            ident="t_antimagical",
            name="Antimagical",
            rules="The faction is dwarven or of some other breed of skilled counter-sorcerers. Assets that require Medium or higher Magic to purchase roll all attribute checks twice against this faction during an Attack and take the worst roll.",  # noqa: E501
        )


class TAGS:
    """Static namespace for Tags."""

    Antimagical = Antimagical()
