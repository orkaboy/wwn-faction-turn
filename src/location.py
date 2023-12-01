from typing import Self


class Location:
    def __init__(self: Self, name: str, uuid: str) -> None:
        self.name = name
        self.uuid = uuid
        self.desc: str = ""
        self.asset_ids: list[str] = []

    def __repr__(self: Self) -> str:
        return self.name
