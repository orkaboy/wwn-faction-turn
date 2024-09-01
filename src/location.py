from typing import Any, Self

from yamlable import YamlAble, yaml_info


@yaml_info(yaml_tag_ns="wwn")
class Location(YamlAble):
    def __init__(
        self: Self,
        name: str,
        uuid: str,
        desc: str = "",
        assets: list[Any] = None,
        bases: list[Any] = None,
    ) -> None:
        self.name = name
        self.uuid = uuid
        self.desc = desc
        self.assets = assets
        if assets is None:
            self.assets = []
        self.bases = bases
        if bases is None:
            self.bases = []

    def __to_yaml_dict__(self: Self) -> dict:
        return {
            "name": self.name,
            "uuid": self.uuid,
            "desc": self.desc,
            "assets": [asset.uuid for asset in self.assets],
            "bases": [base.uuid for base in self.bases],
        }

    def __repr__(self: Self) -> str:
        return self.name
