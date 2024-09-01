from typing import Self

from yamlable import YamlAble, yaml_info

from src.location import Location


@yaml_info(yaml_tag_ns="wwn")
class BaseOfInfluence(YamlAble):
    """A faction's base of influence."""

    def __init__(
        self: Self,
        uuid: str,
        owner: str,
        location: Location | str,
        max_hp: int,
        hp: int = None,
        desc: str = "",
    ) -> None:
        """Initialize BaseOfInfluence object."""
        self.uuid = uuid
        self.owner = owner
        self.location = location
        self.max_hp = max_hp
        self.hp = hp
        if hp is None:
            self.hp = max_hp
        self.desc: str = desc

    def __to_yaml_dict__(self: Self) -> dict:
        loc = self.location.uuid if self.location else None
        return {
            "uuid": self.uuid,
            "owner": self.owner,
            "location": loc,  # Note, needs to be linked
            "max_hp": self.max_hp,
            "hp": self.hp,
            "desc": self.desc,
        }
