from typing import Self

from imgui_bundle import imgui


class TagPrototype:
    def __init__(self: Self, ident: str, name: str, rules: str) -> None:
        """Initialize TagPrototype object."""
        self.id = ident
        self.name = name
        self.rules = rules


class Tag:
    def __init__(
        self: Self,
        prototype: TagPrototype,
    ) -> None:
        """Initialize Tag object."""
        self.prototype = prototype

    def render(self: Self) -> None:
        imgui.text(self.prototype.name)
        imgui.text_wrapped(self.prototype.rules)
