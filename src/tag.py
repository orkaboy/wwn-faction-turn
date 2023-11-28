from typing import Self


class Tag:
    def __init__(self: Self, ident: str, name: str) -> None:
        """Initialize Tag object."""
        self.id = ident
        self.name = name

    def render(self: Self, idx: str) -> None:
        pass
