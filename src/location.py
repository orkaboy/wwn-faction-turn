from typing import Any, Self


class Location:
    def __init__(self: Self, name: str, uuid: str) -> None:
        self.name = name
        self.uuid = uuid
        self.desc: str = ""
        self.assets: list[Any] = []
        self.bases: list[Any] = []

    def __repr__(self: Self) -> str:
        return self.name
