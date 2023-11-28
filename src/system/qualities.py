from typing import Self

from src.mapper import get_class_values
from src.quality import Quality


class Stealth(Quality):
    def __init__(self: Self) -> None:
        super().__init__(
            name="Stealth",
            ident="q_stealth",
        )


class Subtle(Quality):
    def __init__(self: Self) -> None:
        super().__init__(
            name="Subtle",
            ident="q_subtle",
        )


class QUALITY:
    """Static namespace for Qualities."""

    Stealth = Stealth()
    Subtle = Subtle()


_quality = get_class_values(QUALITY)


def quality_list() -> list[QUALITY]:
    return _quality
