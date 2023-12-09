from typing import Self

from src.location import Location


class BaseOfInfluence:
    """A faction's base of influence."""

    def __init__(self: Self, uuid: str, owner: str, location: Location, max_hp: int) -> None:
        """Intialize BaseOfInfluence object."""
        self.uuid = uuid
        self.owner = owner
        self.location = location
        self.max_hp = max_hp
        self.hp = max_hp
        self.desc: str = ""
