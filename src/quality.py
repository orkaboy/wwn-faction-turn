from typing import Self


class Quality:
    def __init__(
        self: Self,
        name: str,
        ident: str,
        rules: str,
        persistent: bool = True,
    ) -> None:
        """Instantiate Quality object."""
        self.name = name
        self.id = ident
        self.rules = rules
        self.persistent = persistent
